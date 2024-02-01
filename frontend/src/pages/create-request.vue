<script setup lang="ts">
import { ref } from 'vue';

const basePath = '/images/icons/integrations/';
const chatUrl = ref(`${basePath}chat-gpt.svg`);
const gmailUrl = ref(`${basePath}gmail.svg`);
const trelloUrl = ref(`${basePath}trello.svg`);
const slackUrl = ref(`${basePath}slack.svg`);
const hubspotUrl = ref(`${basePath}hubspot.svg`);
const mailchimpUrl = ref(`${basePath}mailchimp.svg`);
const salesforceUrl = ref(`${basePath}salesforce.svg`);
const googledriveUrl = ref(`${basePath}google-drive.svg`);
const facebookUrl = ref(`${basePath}facebook.svg`);

</script>

<template>
  <div class="container">
    <div class="upper-division">
      <div class="form-wrapper">
        <h1 class="title">Create Request</h1>
        <CreateRequestBox />
      </div>
    </div>
    <div class="horizontal-line"></div>

    <div class="lower-division">

      <div class="template-grid-container">
        <div class="template-title">

          Templates

        </div>
        <div class="template-grid-row">
          <TemplateCard title="Add notes to the customer's service file" :image1="chatUrl" :image2="googledriveUrl" />
          <TemplateCard title="Configure customer inquiries from Facebook ad as new leads" :image1="facebookUrl"
            :image2="salesforceUrl" />
          <TemplateCard title="Put customer issues from Gmail into Trello Board" :image1="slackUrl" :image2="trelloUrl" />
        </div>
        <div class="template-grid-row">
          <TemplateCard title="Add notes to the customer's service file" :image1="gmailUrl" :image2="trelloUrl" />
          <TemplateCard title="Put customer issues from Gmail into Trello Board" :image1="hubspotUrl"
            :image2="slackUrl" />
          <TemplateCard title="Put customer issues from Gmail into Trello Board" :image1="chatUrl" :image2="trelloUrl" />
        </div>
        <div class="template-grid-row">
          <TemplateCard title="Add notes to the customer's service file" :image1="hubspotUrl" :image2="trelloUrl" />
          <TemplateCard title="Put customer issues from Gmail into Trello Board" :image1="chatUrl" :image2="slackUrl" />
          <TemplateCard title="Put customer issues from Gmail into Trello Board" :image1="gmailUrl"
            :image2="mailchimpUrl" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

.container {
  display: flex;
  flex-direction: column;
  height: 130vh;
  /* Use viewport height to make container fill the screen */
  background-color: #fff;
}

.upper-division {
  display: flex;
  /* Make it a flex container */
  justify-content: center;
  /* Center horizontally */
  align-items: center;
  /* Center vertically */
  flex: 6;
  /* Flex property to take the needed space */
  background-image: url('@images/svg/dot-grid.svg');
  /* Your dot-grid background */
  padding-bottom: 3rem;
  padding-top: 2rem;
  background-color: #FAFAF7;
}

.title {
  font-size: 3.4rem;
  font-weight: 500;
  margin-bottom: -10px;
  color: var(--light-solid-color-gray-gray-500-hover, #656565);
}

.form-wrapper {
  position: relative;
  display: flex;
  flex-direction: column;
  /* Remove margin-top if you want to truly center it, as margin-top will offset it */
  width: 100%;
  max-width: 864px;
  /* Your set width for the form */
  padding-bottom: 2rem;
}

.horizontal-line {
  background-color: #dbdade;
  width: calc(100% + 10rem);
  min-height: 1.5px;
  margin-left: -5rem;
  margin-right: -5rem;
}

.page-content-container {
  width: 102%
}

.lower-division {
  display: flex;
  flex-direction: column;
  align-items: center; /* Center children horizontally */
  background-color: #fff;  margin-left: -5rem;
  margin-right: -5rem;
  margin-bottom: -5rem;
  
}

.template-grid-container {
  width: 60%; /* Maintain desired width */
  padding-bottom: 8rem;
  flex-direction: column; /* Stack children vertically */
  align-items: center; /* Center children horizontally */
  gap: 1rem;
  padding: 1rem;
}

.template-title {
  font-size: 2.2rem;
  font-weight: 500;
  color: var(--light-solid-color-gray-gray-500-hover, #656565);
  align-self: center;
  padding-top: 0.8rem;
  padding-bottom: 0.2rem;
}

.template-grid-row {
  padding: 0.5rem;
  display: flex;
  justify-content: space-between;
  }
</style>