<script setup lang="ts">
const isDialogVisible = ref(false);
</script>

<template>
  <VDialog v-model="isDialogVisible" width="auto">
    <!-- Activator -->
    <template #activator="{ props }">
      <VBtn prepend-icon="tabler:circle-plus" color='success' class=" border" v-bind="props"> Add task </VBtn>
    </template>

    <!-- Dialog close btn -->
    <DialogCloseBtn @click="isDialogVisible = false" />

    <!-- Dialog Content -->
    <VCard>
      <VRow>
        <!-- Search buttons -->
        <VCol class="py-10 px-6" cols="12" md="2">
          <div class="d-flex flex-column align-start gap-4">
            <VBtn variant="text">All</VBtn>
            <VBtn variant="text">Defaults</VBtn>
            <VBtn variant="text">Your tasks</VBtn>
          </div>
        </VCol>

        <!-- Cards -->
        <VCol class="py-10 px-6" cols="12" md="10">
          <VRow>
            <!-- Example card -->
            <VCol cols="12" sm="6" md="4">
              <VCard title="Look up details" subtitle="look_up_details">
                <VCardText>
                  Some quick example text to build on the card title and make up
                  the bulk of the card's content.

                  <div class="mt-4 d-flex gap-3">
                    <VBtn prepend-icon="tabler:circle-plus" color='success'> Add task </VBtn>
                    <VBtn prepend-icon="tabler:info-circle" color="secondary">
                      Info
                    </VBtn>
                  </div>
                </VCardText>
              </VCard>
            </VCol>

            <!-- Example card -->
            <VCol cols="12" sm="6" md="4">
              <VCard title="Look up details" subtitle="look_up_details">
                <VCardText>
                  Some quick example text to build on the card title and make up
                  the bulk of the card's content.

                  <div class="mt-4 d-flex gap-3">
                    <VBtn prepend-icon="tabler:circle-plus" color='success'> Add task </VBtn>
                    <VBtn prepend-icon="tabler:info-circle" color="secondary">
                      Info
                    </VBtn>
                  </div>
                </VCardText>
              </VCard>
            </VCol>

            <!-- Example card -->
            <VCol cols="12" sm="6" md="4">
              <VCard title="Look up details" subtitle="look_up_details">
                <VCardText>
                  Some quick example text to build on the card title and make up
                  the bulk of the card's content.

                  <div class="mt-4 d-flex gap-3">
                    <VBtn prepend-icon="tabler:circle-plus" color='success'> Add task </VBtn>
                    <VBtn prepend-icon="tabler:info-circle" color="secondary">
                      Info
                    </VBtn>
                  </div>
                </VCardText>
              </VCard>
            </VCol>
          </VRow>

          <VRow>
            <!-- Example card -->
            <VCol cols="12" sm="6" md="4">
              <VCard title="Look up details" subtitle="look_up_details">
                <VCardText>
                  Some quick example text to build on the card title and make up
                  the bulk of the card's content.

                  <div class="mt-4 d-flex gap-3">
                    <VBtn prepend-icon="tabler:circle-plus" color='success'> Add task </VBtn>
                    <VBtn prepend-icon="tabler:info-circle" color="secondary">
                      Info
                    </VBtn>
                  </div>
                </VCardText>
              </VCard>
            </VCol>

            <!-- Example card -->
            <VCol cols="12" sm="6" md="4">
              <VCard title="Look up details" subtitle="look_up_details">
                <VCardText>
                  Some quick example text to build on the card title and make up
                  the bulk of the card's content.

                  <div class="mt-4 d-flex gap-3">
                    <VBtn prepend-icon="tabler:circle-plus" color='success'> Add task </VBtn>
                    <VBtn prepend-icon="tabler:info-circle" color="secondary">
                      Info
                    </VBtn>
                  </div>
                </VCardText>
              </VCard>
            </VCol>

            <!-- Example card -->
            <VCol cols="12" sm="6" md="4">
              <VCard title="Look up details" subtitle="look_up_details">
                <VCardText>
                  Some quick example text to build on the card title and make up
                  the bulk of the card's content.

                  <div class="mt-4 d-flex gap-3">
                    <VBtn prepend-icon="tabler:circle-plus" color='success'> Add task </VBtn>
                    <VBtn prepend-icon="tabler:info-circle" color="secondary">
                      Info
                    </VBtn>
                  </div>
                </VCardText>
              </VCard>
            </VCol>
          </VRow>
        </VCol>
      </VRow>
    </VCard>
  </VDialog>
</template>
