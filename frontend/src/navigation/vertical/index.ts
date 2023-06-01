import type { VerticalNavItems } from "@/@layouts/types";

export default [
  {
    title: "Home",
    to: { name: "index" },
    icon: { icon: "tabler-smart-home" },
  },
  {
    title: "Create Flow",
    to: { name: "workflow-create" },
    icon: { icon: "tabler:file" },
  },
  {
    title: "Second page",
    icon: { icon: "tabler-file" },
    children: [
      {
        title: "Second Page",
        icon: { icon: "material-symbols:10k-outline" },
        to: { name: "second-page" },
      },
    ],
  },
] as VerticalNavItems;
