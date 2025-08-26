import React, { ComponentType } from 'react';

type SvgComponent = {
  default: ComponentType<any>;
};

type SvgStats = Record<string, () => Promise<unknown>>;

const FailedLoadSvg = () => {
  console.log('Failed to load SVG component');
  return <div></div>;
};

const isRemoteUrl = (path: string): boolean =>
  /^https?:\/\//.test(path);

const createSvgComponentFromText = (svgText: string): ComponentType<React.SVGProps<SVGSVGElement>> => {
  const parser = new DOMParser();
  const svgDoc = parser.parseFromString(svgText, 'image/svg+xml');

  // Check for parsing errors
  const parserError = svgDoc.querySelector('parsererror');
  if (parserError) {
    throw new Error(`Invalid SVG: ${parserError.textContent}`);
  }

  const svgElement = svgDoc.documentElement;

  // Extract SVG attributes more efficiently
  const attributes = Array.from(svgElement.attributes).reduce(
    (acc, attr) => ({ ...acc, [attr.name]: attr.value }),
    {}
  );

  return (props: React.SVGProps<SVGSVGElement>) => (
    <svg
      {...attributes}
      {...props}
      dangerouslySetInnerHTML={{ __html: svgElement.innerHTML }}
    />
  );
};

export const loadSvgComponent = async (
  stats: SvgStats,
  path: string
): Promise<SvgComponent> => {
  try {
    if (isRemoteUrl(path)) {
      const response = await fetch(path);

      if (!response.ok) {
        throw new Error(`Failed to fetch SVG: ${response.statusText}`);
      }

      const svgText = await response.text();
      return { default: createSvgComponentFromText(svgText) };
    }

    const module = await stats[path]();
    return { default: module as ComponentType<any> };
  } catch (error) {
    console.error(`Error loading SVG from ${path}:`, error);
    return { default: FailedLoadSvg };
  }
};