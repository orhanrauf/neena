<script setup lang="ts">
import { VDataTable } from "vuetify/labs/VDataTable";

const options = ref({
  page: 1,
  itemsPerPage: 10,
  sortBy: [""],
  sortDesc: [false],
});
const search = ref("");

// Items per page options
const itemsPerPage = [5, 10, 25, 50, 100];

// Geaders
const headers = [
  { title: "NAME", key: "name" },
  { title: "PARAMETERS", key: "parameters" },
  { title: "CREATED DATE", key: "created_date" },
  { title: "TAGS", key: "tags" },
  { title: "", key: "actions", sortable: false },
];

// Data
const items = [
  {
    name: "view_detail",
    parameters: '<span class="text-green">string:</span> detail',
    created_date: "09 May 2022",
    tags: "system",
  },
  {
    name: "lookup_acc_number_by_email",
    parameters: '<span class="text-green">string:</span> email',
    created_date: "19 Nov 2022",
    tags: "custom, python, db",
  },
  {
    name: "send_confirmation_email",
    parameters:
      '<span class="text-purple">bool:</span> confirmed, <span class="text-green">string:</span> messa...',
    created_date: "25 Sep 2022",
    tags: "custom, python, mail",
  },
  {
    name: "view_detail",
    parameters: '<span class="text-green">string:</span> detail',
    created_date: "09 May 2022",
    tags: "system",
  },
  {
    name: "verify_age",
    parameters: '<span class="text-blue">int:</span> age',
    created_date: "25 Sep 2022",
    tags: "custom, python, subs...",
  },
  {
    name: "view_detail",
    parameters: '<span class="text-green">string:</span> detail',
    created_date: "09 May 2022",
    tags: "system",
  },
  {
    name: "view_detail",
    parameters: '<span class="text-green">string:</span> detail',
    created_date: "09 May 2022",
    tags: "system",
  },
  {
    name: "verify_age",
    parameters: '<span class="text-blue">int:</span> age',
    created_date: "25 Sep 2022",
    tags: "custom, python, subs...",
  },
  {
    name: "view_detail",
    parameters: '<span class="text-green">string:</span> detail',
    created_date: "09 May 2022",
    tags: "system",
  },
  {
    name: "view_detail",
    parameters: '<span class="text-green">string:</span> detail',
    created_date: "09 May 2022",
    tags: "system",
  },
  {
    name: "verify_age",
    parameters: '<span class="text-blue">int:</span> age',
    created_date: "25 Sep 2022",
    tags: "custom, python, subs...",
  },
  // Additional items
  {
    name: "lookup_account_by_id",
    parameters: '<span class="text-green">string:</span> id',
    created_date: "12 Dec 2022",
    tags: "custom, db",
  },
  {
    name: "send_notification_email",
    parameters: '<span class="text-green">string:</span> email',
    created_date: "29 Nov 2022",
    tags: "custom, mail",
  },
  {
    name: "update_profile",
    parameters:
      '<span class="text-purple">bool:</span> isPublic, <span class="text-green">string:</span> name',
    created_date: "05 Jan 2023",
    tags: "custom, profile",
  },
  {
    name: "calculate_total",
    parameters: '<span class="text-blue">int:</span> quantity',
    created_date: "18 Feb 2023",
    tags: "custom, math",
  },
  {
    name: "send_reset_password_email",
    parameters: '<span class="text-green">string:</span> email',
    created_date: "02 Mar 2023",
    tags: "custom, mail",
  },
  {
    name: "lookup_product_by_sku",
    parameters: '<span class="text-green">string:</span> sku',
    created_date: "15 Apr 2023",
    tags: "custom, inventory",
  },
  {
    name: "process_payment",
    parameters:
      '<span class="text-purple">bool:</span> isPaid, <span class="text-green">string:</span> paymentMethod',
    created_date: "28 May 2023",
    tags: "custom, payment",
  },
  {
    name: "send_notification_sms",
    parameters: '<span class="text-green">string:</span> phoneNumber',
    created_date: "10 Jun 2023",
    tags: "custom, sms",
  },
  {
    name: "calculate_discount",
    parameters: '<span class="text-blue">int:</span> amount',
    created_date: "23 Jun 2023",
    tags: "custom, math",
  },
  {
    name: "lookup_order_by_id",
    parameters: '<span class="text-green">string:</span> orderId',
    created_date: "06 Jul 2023",
    tags: "custom, db",
  },
];
</script>

<template>
  <VCard class=" border">
    <!-- Filters -->
    <VCardText>
      <VRow>
        <VCol cols="12" md="4">
          <AppTextField
            v-model="search"
            density="compact"
            placeholder="Search Task"
            append-inner-icon="tabler-search"
            single-line
            hide-details
            dense
            outlined
          />
        </VCol>

        <VCol cols="12" offset-md="4" md="2">
          <VSelect label="Select tags" />
        </VCol>
        <VCol cols="12" md="2">
          <VSelect :items="itemsPerPage" v-model="options.itemsPerPage" />
        </VCol>
      </VRow>
    </VCardText>

    <!-- Data Table  -->
    <VDataTable
      :headers="headers"
      :items="items"
      :search="search"
      :items-per-page="options.itemsPerPage"
      :page="options.page"
      @update:options="options = $event"
    >
      <!-- Name -->
      <template #item.name="{ item }">
        <span class="text-prim" v-html="item.value.name"></span>
      </template>

      <!-- Parameters -->
      <template #item.parameters="{ item }">
        <span v-html="item.value.parameters"></span>
      </template>

      <!-- Actions -->
      <template #item.actions="{ item }">
        <button class="mx-1" @click="undefined">
          <VIcon icon="tabler-mail" size="26" />
        </button>
        <button class="mx-1" @click="undefined">
          <VIcon icon="tabler-eye" size="26" />
        </button>
        <button class="mx-1" @click="undefined">
          <VIcon icon="tabler-dots-vertical" size="26" />
        </button>
      </template>

      <!-- Datatable footer -->
      <template #bottom>
        <VCardText class="pt-4">
          <VRow>
            <VCol lg="2" cols="3">
              <p style="font-size: 14px">
                Showing 1 to 10 of {{ items.length }} entries
              </p>
            </VCol>

            <VCol lg="10" cols="9" class="d-flex justify-end">
              <VPagination
                
                v-model="options.page"
                total-visible="5"
                :length="Math.ceil(items.length / options.itemsPerPage)"
              />
            </VCol>
          </VRow>
        </VCardText>
      </template>
    </VDataTable>
  </VCard>
</template>

<style>
.text-prim {
  color: #67b6f0 !important;
}

.text-green {
  color: #28c76f !important;
}

.text-blue {
  color: #67b6f0 !important;
}

.text-purple {
  color: #7367f0 !important;
}
</style>
