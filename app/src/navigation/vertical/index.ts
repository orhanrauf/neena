import type { VerticalNavItems } from '@/@layouts/types'

export default [
  {
    title: 'Home',
    to: { name: 'index' },
    icon: { icon: 'tabler-smart-home' },
  },
  {
    title: 'Second page',
    icon: { icon: 'tabler-file' },
    children: [
      {
        title: 'Second Page',
        icon: { icon: 'material-symbols:10k-outline' },
        to: { name: 'second-page' },
      },
    ],
  },
] as VerticalNavItems
