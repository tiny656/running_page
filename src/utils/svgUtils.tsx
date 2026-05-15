import type { ComponentType, SVGProps } from 'react';

type SvgComponentType = ComponentType<SVGProps<SVGSVGElement>>;
type SvgComponent = {
  default: SvgComponentType;
};

const FailedLoadSvg: SvgComponentType = () => null;

const isRemoteUrl = (path: string): boolean => /^https?:\/\//.test(path);

const createSvgComponentFromText = (
  svgText: string,
  displayName = 'InlineSvgFromText'
): SvgComponentType => {
  const parser = new DOMParser();
  const svgDoc = parser.parseFromString(svgText, 'image/svg+xml');

  const parserError = svgDoc.querySelector('parsererror');
  if (parserError) {
    throw new Error(`Invalid SVG: ${parserError.textContent}`);
  }

  const svgElement = svgDoc.documentElement;
  const attributes = Array.from(svgElement.attributes).reduce<
    Record<string, string>
  >((acc, attr) => {
    acc[attr.name] = attr.value;
    return acc;
  }, {});

  const SvgFromText: SvgComponentType = (props) => (
    <svg
      {...attributes}
      {...props}
      dangerouslySetInnerHTML={{ __html: svgElement.innerHTML }}
    />
  );

  SvgFromText.displayName = displayName;
  return SvgFromText;
};

export const loadSvgComponent = async (
  stats: Record<string, () => Promise<unknown>>,
  path: string
): Promise<SvgComponent> => {
  try {
    if (isRemoteUrl(path)) {
      const response = await fetch(path);
      if (!response.ok) {
        throw new Error(`Failed to fetch SVG: ${response.statusText}`);
      }
      const svgText = await response.text();
      let name = 'InlineSvgFromText';
      try {
        const url = new URL(path);
        const fname = (url.pathname.split('/').pop() || '').replace(
          /\.[a-z]+$/i,
          ''
        );
        if (fname) name = `Svg(${fname})`;
      } catch {
        // Use default name if URL parsing fails
      }
      return { default: createSvgComponentFromText(svgText, name) };
    }

    const module = await stats[path]();
    return { default: module as SvgComponentType };
  } catch (error) {
    console.error(error);
    return { default: FailedLoadSvg };
  }
};
