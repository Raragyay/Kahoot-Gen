const CracoLessPlugin = require('craco-less');
const purgecss = require('@fullhuman/postcss-purgecss');

module.exports = {
    style: {
        postcss: {
            plugins: [
                purgecss({
                    content: ['./src/**/*.html', './src/**/*.jsx', './src/**/*.js', './src/**/*.ts', './src/**/*.tsx']
                })
            ]
        }
    },
    plugins: [
        {
            plugin: CracoLessPlugin,
            options: {
                lessLoaderOptions: {
                    lessOptions: {
                        javascriptEnabled: true,
                    },
                },
            },
        },
    ],
};