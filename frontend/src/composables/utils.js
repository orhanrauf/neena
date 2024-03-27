/**
 * Retrieves a task definition by its ID.
 *
 * @param {string} taskDefinitionId - The ID of the task definition to retrieve.
 * @returns {Promise<Object>} - A promise that resolves to the task definition object.
 * @throws {Error} - If an error occurs while retrieving the task definition.
 */
async function getTaskDefinitionById(taskDefinitionId) {

    try {
        const response = await http.get(`task_definitions?id=${taskDefinitionId}`);
        return response.data;
    } catch (error) {
        console.error('Error getting task definition:', error);
        throw error;
    }
}

export default getTaskDefinition;