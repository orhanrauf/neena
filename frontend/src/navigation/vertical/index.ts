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
    title: "Task",
    to: { name: "task" },
    icon: { icon: "tabler:file-description" },
  },
  {
    title: "Tasks",
    to: { name: "tasks" },
    icon: { icon: "tabler:file-description" },
  },
  {
    title: "Task names",
    to: { name: "tasknames-create" },
    icon: { icon: "tabler:file-description" },
  },
] as VerticalNavItems;
