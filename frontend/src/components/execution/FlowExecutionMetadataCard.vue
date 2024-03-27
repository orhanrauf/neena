<script>
const response = ref(null);
</script>

<template>
    <VCard class="mb-4">
        <VCardText>
            <div>
                <h4 class="mb-3 card-subheading">DETAILS</h4>
                <div class="d-flex align-center my-1">
                    <span class="mr-2">
                        <VIcon
                            icon="tabler-user"
                            color="#4B465C"
                            size="18"
                        />
                    </span>
                    <span class="mr-1 card-property-text">
                        Created by:
                    </span>
                    <span class="card-value-text">
                        John Doe
                    </span>
                </div>
                <div class="d-flex align-center my-1">
                    <span class="mr-2">
                        <VIcon
                            icon="tabler-check"
                            size="18"
                            color="#4B465C"
                        />
                    </span>
                    <span class="mr-2 card-property-text">
                        Has Flow:
                    </span>
                    <span
                        class="has-flow"
                        :class="
                            response?.flow
                                ? 'has-flow-yes'
                                : 'has-flow-no'
                        "
                    >
                        {{ response?.flow ? 'Yes' : 'No' }}
                    </span>
                </div>
                <div class="d-flex align-center my-1">
                    <span class="mr-2">
                        <VIcon
                            icon="tabler-message-circle"
                            size="18"
                            color="#4B465C"
                        />
                    </span>
                    <span class="mr-1 card-property-text">
                        Source:
                    </span>
                    <span class="card-value-text">
                        User Interface
                    </span>
                </div>
                <div class="d-flex align-center my-1">
                    <span class="mr-2">
                        <VIcon
                            icon="tabler-clock-hour-4"
                            size="18"
                            color="#4B465C"
                        />
                    </span>
                    <span class="mr-1 card-property-text">
                        Country:
                    </span>
                    <span class="card-value-text">USA</span>
                </div>
                <div class="d-flex align-center my-1">
                    <span class="mr-2">
                        <VIcon
                            icon="tabler-language"
                            size="18"
                            color="#4B465C"
                        />
                    </span>
                    <span class="mr-1 card-property-text">
                        Languages:
                    </span>
                    <span class="card-value-text">English</span>
                </div>
            </div>
            <div class="mt-4">
                <h4 class="mb-3 card-subheading">
                    PLACEHOLDER DETAILS
                </h4>
                <div class="d-flex align-center my-1">
                    <span class="mr-2">
                        <VIcon
                            icon="tabler-phone-call"
                            color="#4B465C"
                            size="18"
                        />
                    </span>
                    <span class="mr-1 card-property-text">
                        Contact:
                    </span>
                    <span class="card-value-text">
                        (123) 456-7890
                    </span>
                </div>
                <div class="d-flex align-center my-1">
                    <span class="mr-2">
                        <VIcon
                            icon="tabler-brand-skype"
                            size="18"
                            color="#4B465C"
                        />
                    </span>
                    <span class="mr-1 card-property-text">
                        Skype:
                    </span>
                    <span class="card-value-text">
                        john.doe
                    </span>
                </div>
                <div class="d-flex align-center my-1">
                    <span class="mr-2">
                        <VIcon
                            icon="tabler-mail"
                            size="18"
                            color="#4B465C"
                        />
                    </span>
                    <span class="mr-1 card-property-text">
                        Email:
                    </span>
                    <span class="card-value-text">
                        {{ response?.created_by_email }}
                    </span>
                </div>
            </div>
            <div class="mt-4">
                <h4 class="mb-3 card-subheading">
                    PLACEHOLDERS
                </h4>
                <div class="d-flex align-center my-1">
                    <span class="mr-2">
                        <VIcon
                            icon="tabler-brand-angular"
                            color="#EA5455"
                            size="18"
                        />
                    </span>
                    <span class="mr-1 card-property-text">
                        Backend Developer:
                    </span>
                    <span class="card-value-text">
                        (126 Members)
                    </span>
                </div>
                <div class="d-flex align-center my-1">
                    <span class="mr-2">
                        <VIcon
                            icon="tabler-brand-react"
                            size="18"
                            color="#00CFE8"
                        />
                    </span>
                    <span class="mr-1 card-property-text">
                        React Developer:
                    </span>
                    <span class="card-value-text">
                        (98 Members)
                    </span>
                </div>
            </div>
        </VCardText>
    </VCard>

    <VCard>
        <VCardText>
            <div>
                <h4 class="mb-3 card-subheading">DETAILS</h4>
                <div class="d-flex align-center my-1">
                    <span class="mr-2">
                        <VIcon
                            icon="tabler-user"
                            color="#4B465C"
                            size="18"
                        />
                    </span>
                    <span class="mr-1 card-property-text">
                        Created by:
                    </span>
                    <span class="card-value-text">
                        John Doe
                    </span>
                </div>
                <div class="d-flex align-center my-1">
                    <span class="mr-2">
                        <VIcon
                            icon="tabler-check"
                            size="18"
                            color="#4B465C"
                        />
                    </span>
                    <span class="mr-2 card-property-text">
                        Has Flow:
                    </span>
                    <span
                        class="has-flow"
                        :class="
                            response?.flow
                                ? 'has-flow-yes'
                                : 'has-flow-no'
                        "
                    >
                        {{ response?.flow ? 'Yes' : 'No' }}
                    </span>
                </div>
                <div class="d-flex align-center my-1">
                    <span class="mr-2">
                        <VIcon
                            icon="tabler-message-circle"
                            size="18"
                            color="#4B465C"
                        />
                    </span>
                    <span class="mr-1 card-property-text">
                        Source:
                    </span>
                    <span class="card-value-text">
                        User Interface
                    </span>
                </div>
                <div class="d-flex align-center my-1">
                    <span class="mr-2">
                        <VIcon
                            icon="tabler-clock-hour-4"
                            size="18"
                            color="#4B465C"
                        />
                    </span>
                    <span class="mr-1 card-property-text">
                        Country:
                    </span>
                    <span class="card-value-text">USA</span>
                </div>
                <div class="d-flex align-center my-1">
                    <span class="mr-2">
                        <VIcon
                            icon="tabler-language"
                            size="18"
                            color="#4B465C"
                        />
                    </span>
                    <span class="mr-1 card-property-text">
                        Languages:
                    </span>
                    <span class="card-value-text">English</span>
                </div>
            </div>
            <div class="mt-4">
                <h4 class="mb-3 card-subheading">
                    PLACEHOLDER DETAILS
                </h4>
                <div class="d-flex align-center my-1">
                    <span class="mr-2">
                        <VIcon
                            icon="tabler-phone-call"
                            color="#4B465C"
                            size="18"
                        />
                    </span>
                    <span class="mr-1 card-property-text">
                        Contact:
                    </span>
                    <span class="card-value-text">
                        (123) 456-7890
                    </span>
                </div>
                <div class="d-flex align-center my-1">
                    <span class="mr-2">
                        <VIcon
                            icon="tabler-brand-skype"
                            size="18"
                            color="#4B465C"
                        />
                    </span>
                    <span class="mr-1 card-property-text">
                        Skype:
                    </span>
                    <span class="card-value-text">
                        john.doe
                    </span>
                </div>
                <div class="d-flex align-center my-1">
                    <span class="mr-2">
                        <VIcon
                            icon="tabler-mail"
                            size="18"
                            color="#4B465C"
                        />
                    </span>
                    <span class="mr-1 card-property-text">
                        Email:
                    </span>
                    <span class="card-value-text">
                        {{ response?.created_by_email }}
                    </span>
                </div>
            </div>
        </VCardText>
    </VCard>
  </template>