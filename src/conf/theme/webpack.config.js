const webpack = require('webpack');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const TerserJSPlugin = require('terser-webpack-plugin');
const OptimizeCSSAssetsPlugin = require('optimize-css-assets-webpack-plugin');
const RtlCssPlugin = require('rtlcss-webpack-plugin');
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');
const BundleTracker = require('webpack-bundle-tracker');

const path = require('path');

// const autoprefixerBrowsers = require('bootstrap/package.json').browserslist;
// console.log(autoprefixerBrowsers);
let config = {
    entry: {
        'bundle': [
            path.resolve(__dirname, 'js/app.js'),
        ]
    },
    output: {
        publicPath: '/static/',
        filename: 'js/[name]_[hash].js',
        chunkFilename: 'js/modules/[name]_[hash].js',
        path: path.resolve(path.dirname(__dirname), 'static')
    },
    plugins: [
        new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery'
        }),
        new MiniCssExtractPlugin({
            filename: 'css/[name]_[hash].ltr.css',
        }),
        new RtlCssPlugin({
            filename: 'css/[name]_[hash].rtl.css',
        }),
        new BundleTracker({path: path.resolve(path.dirname(__dirname), 'static'), filename: './webpack-stats.json'})
    ],
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /(node_modules|bower_components)/,
                loader: 'babel-loader',
            },
            {
                test: /\.(scss|sass)$/,
                exclude: /\.rtl\.(scss|sass)$/,
                use: [
                    {
                        loader: MiniCssExtractPlugin.loader
                    },
                    {
                        loader: 'css-loader',
                    },
                    {
                        loader: 'postcss-loader',
                        options: {
                            plugins: [
                                require('precss'),
                                require('autoprefixer')(),
                            ]
                        }
                    },
                    {
                        loader: 'sass-loader',
                    }
                ]
            },
            {
                test: require.resolve('jquery'),
                use: [{
                    loader: 'expose-loader',
                    options: 'jQuery'
                }, {
                    loader: 'expose-loader',
                    options: '$'
                }]
            },
            {
                test: /\.woff2?(\?v=[0-9]\.[0-9]\.[0-9])?$/,
                loader: "url-loader",
                options: {
                    limit: 10000,
                    name: '[name].[ext]',
                    outputPath: 'fonts/',
                    // publicPath: 'fonts/'
                }
            },
            {
                test: /\.(otf|ttf|eot)(\?[\s\S]+)?$/,
                loader: "url-loader",
                options: {
                    limit: 10000,
                    name: '[name].[ext]',
                    outputPath: 'fonts/',
                    // publicPath: 'fonts/'
                }
            },
            {
                test: /\.(png|jpg|jpeg|svg)$/,
                loader: 'file-loader',
                options: {
                    outputPath: 'img/',
                    // publicPath: 'img/',
                    name: '[name]_[hash].[ext]'
                }
            },
            {
                test: /\.(mp3)$/,
                loader: 'file-loader',
                options: {
                    outputPath: 'sounds/',
                    // publicPath: '/sounds/',
                    name: '[name].[ext]'
                }
            },

        ]
    },
    optimization: {
        minimizer: [
            // new TerserJSPlugin({}),
            new UglifyJsPlugin({
                uglifyOptions: {
                    output: {
                        comments: false,
                    },
                },
                extractComments: true
            }),
            // new OptimizeCSSAssetsPlugin({
            //     cssProcessor: require('cssnano'),
            //     cssProcessorPluginOptions: {
            //         preset: ['default', {discardComments: false}],
            //     },
            // }),
        ],
        splitChunks: {
            chunks: 'async',
            minSize: 30000,
            maxSize: 0,
            minChunks: 1,
            maxAsyncRequests: 10,
            maxInitialRequests: 10,
            automaticNameDelimiter: '-',
            name: true,
            cacheGroups: {
                default: {
                    minChunks: 2,
                    priority: -20,
                    reuseExistingChunk: true
                }
            }
        }
    },
    devServer: {
        publicPath: "/static/",
        host: "0.0.0.0",
        port: "3000",
        proxy: {
            "*": "http://django:8000"
        },
        watchOptions: {
            poll: true
        }
    }
};

module.exports = (env, argv) => {
    if (argv.mode === 'development') {
        config.devtool = 'source-map';
    }
    // if (argv.mode === 'production') {
    //     config.output.publicPath = 'https://assets.nn.ps/'
    // }
    return config;
};