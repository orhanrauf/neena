<script setup lang="ts">
import avatar1 from "@images/avatars/avatar-1.png";
import { UserData } from "@/types";

const router = useRouter();
const userData = <UserData>(
  JSON.parse(localStorage.getItem("userData") || "null")
);

const logout = () => {
  // Remove "userData" from localStorage
  localStorage.removeItem("userData");

  // Remove "accessToken" from localStorage
  localStorage.removeItem("accessToken");

  // Redirect to login page
  router.push("/login");
};
</script>

<template>
  <VBadge 
    dot
    location="bottom right"
    offset-x="3"
    offset-y="3"
    bordered
    color="success"
  >
    <VAvatar class="cursor-pointer" color="primary" variant="tonal">
      <VImg :src="avatar1" />

      <!-- SECTION Menu -->
      <VMenu activator="parent" width="230" location="bottom end" offset="14px">
        <VList>
          <!-- 👉 User Avatar & Name -->
          <VListItem>
            <template #prepend>
              <VListItemAction start>
                <VBadge
                  dot
                  location="bottom right"
                  offset-x="3"
                  offset-y="3"
                  color="success"
                >
                  <VAvatar color="primary" variant="tonal">
                    <VImg :src="avatar1" />
                  </VAvatar>
                </VBadge>
              </VListItemAction>
            </template>

            <VListItemTitle class="font-weight-semibold">
              {{ userData.full_name }}
            </VListItemTitle>
            <VListItemSubtitle v-if="userData.is_superuser">
              Admin
            </VListItemSubtitle>
          </VListItem>

          <VDivider class="my-2" />

          <!-- 👉 Logout -->
          <VListItem @click="logout">
            <template #prepend>
              <VIcon class="me-2" icon="tabler-logout" size="22" />
            </template>

            <VListItemTitle>Logout</VListItemTitle>
          </VListItem>
        </VList>
      </VMenu>
      <!-- !SECTION -->
    </VAvatar>
  </VBadge>
</template>
