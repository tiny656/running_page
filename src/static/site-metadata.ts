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
  logo: 'https://ooo.0x0.ooo/2024/12/20/OE5H71.png',
  description: 'RealTiny656 Run',
  navLinks: [
    {
      name: 'Summary',
      url: `${import.meta.env.BASE_URL}/summary`,
    },
    {
      name: 'Github',
      url: 'https://github.com/tiny656',
    },
  ],
};

export default data;
