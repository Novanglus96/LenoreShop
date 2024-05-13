module.exports = {
  chainWebpack: (config) => {
    config.plugin("html").tap((args) => {
      args[0].title = "LenoreShop";
      return args;
    });
  },
  devServer: {
    proxy: {
      "/api": {
        target: "https://back-dev.danielleandjohn.love/api",
        changeOrigin: true,
        pathRewrite: { "^/api": "" },
      },
    },
    allowedHosts: ["front-dev.danielleandjohn.love"],
    https: true,
  },
};
