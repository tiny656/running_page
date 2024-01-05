interface ISiteMetadataResult {
  siteTitle: string;
  siteUrl: string;
  description: string;
  logo: string;
  navLinks: {
    name: string;
    url: string;
  }[];
}

const data: ISiteMetadataResult = {
  siteTitle: 'RealTiny656 Run',
  siteUrl: 'https://tiny656.github.io/running_page/',
  logo: 'https://ooo.0x0.ooo/2023/12/20/OKzpKP.png',
  description: 'RealTiny656 Run',
  navLinks: [
    // {
    //   name: 'About',
    //   url: 'https://github.com/tiny656',
    // },
  ],
};

export default data;