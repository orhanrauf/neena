<script setup lang="ts">
import { TaskDefinition } from "@/types"
import axios from "@axios";
import { VInfiniteScroll } from "vuetify/labs/components";

const emit = defineEmits<{
  (e: "addTask", task: TaskDefinition): void;
}>();

const loading = ref(false);
const filter = ref("");
let taskDefinitions: TaskDefinition[] = reactive([]);
const isDialogVisible = ref(false);

const getTaskDefinitions = async () => {
  const length = taskDefinitions.length;

  return await axios.get("/v1/task_definitions/all", {
    params: {
      skip: length,
      limit: length + 9,
    },
  });
};

const addTask = (taskDefinition: TaskDefinition) => {
  const cloneTaskDefinition = Object.assign({}, taskDefinition);

  emit("addTask", cloneTaskDefinition);
  isDialogVisible.value = false;
};

const load = async ({ done }) => {
  try {
    const { data } = await getTaskDefinitions();

    if (data && data.length > 0) {
      taskDefinitions.push(...data);

      done("ok");
    } else {
      done("empty");
    }
  } catch (error) {
    console.log(error);

    done("error");
  }
};
</script>

<template>
  <VDialog v-model="isDialogVisible" width="auto">
    <!-- Activator -->
    <template #activator="{ props }">
      <VBtn prepend-icon="tabler:circle-plus" v-bind="props"> Add task </VBtn>
    </template>

    <!-- Dialog close btn -->
    <DialogCloseBtn @click="isDialogVisible = false" />

    <!-- Dialog Content -->
    <VCard class="overflow-hidden">
      <div class="d-flex">
        <!-- Search buttons -->
        <div class="py-10 px-6">
          <div class="d-flex flex-column align-start gap-4">
            <VBtn variant="text">All</VBtn>
            <VBtn variant="text" :disabled="filter !== 'defaults'">
              Defaults
            </VBtn>
            <VBtn variant="text" :disabled="filter !== 'your-tasks'">
              Your tasks
            </VBtn>
          </div>
        </div>

        <!-- Cards -->
        <div class="py-10 px-6 flex-1-1">
          <VInfiniteScroll :height="600" :items="taskDefinitions" @load="load">
            <VRow style="margin: 0 !important">
              <!-- Card -->
              <VCol
                v-for="taskDefinition in taskDefinitions"
                :key="taskDefinition.id"
                cols="12"
                sm="6"
                md="4"
              >
                <VCard
                  :title="taskDefinition.task_name"
                  :subtitle="taskDefinition.output_name"
                  class="d-flex flex-column h-100"
                >
                  <VCardText class="d-flex flex-column">
                    <div class="flex-fill">
                      {{ taskDefinition.description }}
                    </div>

                    <div class="mt-4 d-flex gap-3">
                      <VBtn
                        prepend-icon="tabler:circle-plus"
                        @click="addTask(taskDefinition)"
                      >
                        Add task
                      </VBtn>
                      <VBtn prepend-icon="tabler:info-circle" color="secondary">
                        Info
                      </VBtn>
                    </div>
                  </VCardText>
                </VCard>
              </VCol>
            </VRow>
          </VInfiniteScroll>
        </div>
      </div>
    </VCard>
  </VDialog>
</template>
