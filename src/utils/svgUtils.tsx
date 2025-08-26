import { ComponentType } from 'react';

type SvgComponent = {
  default: ComponentType<any>;
};

const FailedLoadSvg = () => {
  console.log('Failed to load SVG component');
  return <div></div>;
};

export const loadSvgComponent = async (
  stats: Record<string, () => Promise<unknown>>,
  path: string
): Promise<SvgComponent> => {
  try {
    // 检查是否是远程 URL
    if (path.startsWith('http://') || path.startsWith('https://')) {
      // 处理远程 SVG
      const response = await fetch(path);
      const svgText = await response.text();

      const RemoteSvgComponent: ComponentType<any> = (props) => (
        <div
          {...props}
          dangerouslySetInnerHTML={{ __html: svgText }}
        />
      );

      return { default: RemoteSvgComponent };
    } else {
      // 处理本地 SVG
      const module = await stats[path]();
      return { default: module as ComponentType<any> };
    }
  } catch (error) {
    console.error(error);
    return { default: FailedLoadSvg };
  }
};