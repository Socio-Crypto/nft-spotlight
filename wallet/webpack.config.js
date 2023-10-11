const path = require("path");
const webpack = require("webpack");

module.exports = {
  entry: "./src/index.js",

  output: {
    path: path.resolve(__dirname, "./static/frontend"),
    filename: "[name].js",
  },
  devtool: 'eval-source-map',// devtool: "source-map",
  module: {
    rules: [
      {
        test: /\.js|.jsx$/,
        exclude: /node_modules/,
        use: "babel-loader",
      },
      {
        test: /\.css$/,
        // exclude: /node_modules/,
        use: ["style-loader", "css-loader"],
      }
    ],
  },
  optimization: {
    minimize: true,
  },
  plugins: [
    new webpack.DefinePlugin({
      "process.env": {
        NODE_ENV: JSON.stringify("development"),
      },
    }),
  ],
};