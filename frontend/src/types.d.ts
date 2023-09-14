export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: "bearer";
}

export interface RegisterResponse {
  accessToken: string;
  userData: object;
  userAbilities: [];
}

export interface UserData {
  email: string;
  is_active: boolean;
  is_superuser: boolean;
  full_name: string;
  id: string;
  password: boolean;
}

export interface FlowRequest {
  id: string;
  request_body: string;
  request_instructions: string;
  created_date: string;
  modified_date: string;
  created_by_email: string;
  modified_by_email: string;
  request_metadata: {}[];
}

export interface TaskDefinition {
  id: string;
  task_name: string;
  parameters: TaskDefinitionParameter[],
  description: string;
  output_type: string;
  python_code: string;
  created_date: string;
  modified_date: string;
  created_by_email: string;
  modified_by_email: string;
  deleted_at: ?string;
}

export interface TaskDefinitionParameter {
  name: string;
  data_type: string;
  position: number;
}

export interface TaskOperation {
  id: string;
  flow: string;
  task_definition: string;
  name: string;
  explanation: string;
  arguments: TaskOperationArgument[],
  x: number;
  y: number;
  z: number;
  created_date: string;
  modified_date: string;
  created_by_email: string;
  modified_by_email: string;
}

export interface TaskOperationArgument {
  name: string;
  data_type: string;
  value: string;
  source: string;
}

export interface Flow {
  id: string;
  flow_request: string;
  name: string;
  task_operations: TaskOperation[],
  created_date: string;
  modified_date: string;
  created_by_email: string;
  modified_by_email: string;
}

export interface FlowRun {
  id: string;
  flow_request: string;
  name: string;
  task_operations: TaskOperation[],
  created_date: string;
  modified_date: string;
  created_by_email: string;
  modified_by_email: string;
}

export interface NodeTaskDefinition {
  name: string;
  pos_x: number;
  pos_y: number;
  class: string;
  html: string;
  typenode: 'vue';
  data: {
    task_definition: TaskDefinition,
  };
  inputs: {}[];
  outputs: {}[];
}
