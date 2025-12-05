export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: ['@nuxt/ui'],
  css: ['~/assets/css/main.css'],
  future: {
    compatibilityVersion: 4
  },
  compatibilityDate: '2024-11-01',
  app: {
    head: {
      title: 'Earthquakes in Türkiye',
      htmlAttrs: {
        lang: 'tr'
      },
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'twitter:card', content: 'summary_large_image' },
        { name: 'twitter:site', content: '@ndrshn' },
        { name: 'twitter:creator', content: '@ndrshn' },
        { name: 'twitter:title', content: "Türkiye'deki Depremler" },
        { name: 'twitter:description', content: '2003 yılından itibaren gerçekleşen depremleri inceleyin.' },
        { name: 'twitter:image', content: 'https://depremler.ndrshn.com/screenshot.jpg' },
        { property: 'og:type', content: 'article' },
        { property: 'og:title', content: "Türkiye'deki Depremler" },
        { property: 'og:description', content: '2003 yılından itibaren gerçekleşen depremleri inceleyin.' },
        { property: 'og:url', content: 'https://depremler.ndrshn.com/' },
        { property: 'og:image', content: 'https://depremler.ndrshn.com/screenshot.jpg' }
      ],
      link: [
        { rel: 'icon', type: 'image/svg+xml', href: '/logo.svg' },
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
        { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900&display=swap' }
      ]
    }
  }
})
