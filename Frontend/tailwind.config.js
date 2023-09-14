/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    colors: {
      'primary' : '#2B3140',
      'background' : '#EAEBEB',
      'menu_primary' : '#97AABD',
      'menu_secondary' : '#5F7A95'
    },
    extend: {},
  },
  plugins: [],
}