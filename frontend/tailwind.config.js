/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}"
  ],
  theme: {
    extend: {
      colors: {
        'bg-primary': '#0B0F19',
        'bg-card': '#0F1724',
        'bg-card-alt': '#121826',
        'accent-blue': '#1E90FF',
        'accent-green': '#22C55E',
        'accent-red': '#FF6B6B',
        'accent-amber': '#F59E0B',
        'accent-orange': '#FB923C',
        'text-secondary': '#7C8CA1',
      },
      fontFamily: {
        sans: ['Inter', 'IBM Plex Sans', 'system-ui', 'sans-serif'],
      },
      borderRadius: {
        'card': '8px',
      }
    },
  },
  plugins: [],
}
