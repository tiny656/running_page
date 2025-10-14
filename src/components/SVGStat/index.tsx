import { lazy, Suspense, useEffect } from 'react';
import { totalStat } from '@assets/index';
import { loadSvgComponent } from '@/utils/svgUtils';
import { initSvgColorAdjustments } from '@/utils/colorUtils';

// Lazy load both github.svg, grid.svg and miles.svg
const GithubSvg = lazy(() => loadSvgComponent(totalStat, './github.svg'));
const GridSvg = lazy(() => loadSvgComponent(totalStat, './grid.svg'));
const MilesSvg = lazy(() =>
  loadSvgComponent(
    totalStat,
    'https://raw.githubusercontent.com/tiny656/miles/master/miles.svg'
  )
);

const SVGStat = () => {
  useEffect(() => {
    // Initialize SVG color adjustments when component mounts
    const timer = setTimeout(() => {
      initSvgColorAdjustments();
    }, 100); // Small delay to ensure SVG is rendered

    return () => clearTimeout(timer);
  }, []);

  return (
    <div id="svgStat">
      <Suspense fallback={<div className="text-center">Loading...</div>}>
        <GithubSvg className="github-svg mt-4 h-auto w-full" />
        <GridSvg className="grid-svg mt-4 h-auto w-full" />
        <MilesSvg className="miles-svg mt-4 h-auto w-full" />
      </Suspense>
    </div>
  );
};

export default SVGStat;
