export interface LoginResponse {
    access_token: string;
    refresh_token: string;
    token_type: "bearer";
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
    request_name: string;
    request_metadata? : {}[];
    created_date?: string; // Optional
    modified_date?: string; // Optional
    created_by_email?: string; // Optional
    modified_by_email?: string; // Optional
  }

  export interface Task {
    id: number;
    task_name: string;
    iconUrl: string;
    task_description: string;
    output_type: string;
    source: string;
  }

  export interface TaskDefinition {
    id: string; 
    name: string;
    human_readable_id: string;
    yml_output: string; 
    output_type: string;
    description: string;
    source: string;
    created_date?: string; // Optional
    modified_date?: string; // Optional
    created_by_email?: string; // Optional
    modified_by_email?: string; // Optional
    deleted_at?: string;
  }

  export interface TaskOperation {
    id?: string;
    drawflow_node_id: int;
    name: string;
    flow?: string;
    task_definition: string;
    instructions: string;
    x: number;
    y: number;
    created_date?: string;
    modified_date?: string;
    created_by_email?: string;
    modified_by_email?: string;
  }

  export interface Flow {
    id: string;
    flow_request: string;
    name: string;
    task_operations: TaskOperation[],
    dependencies: Dependency[],
    created_date?: string;
    modified_date?: string;
    created_by_email?: string;
    modified_by_email?: string;
  }
  
  export interface Dependency {
    id?: string;
    flow?: string;
    source_node_id: int;
    target_node_id: int;
    instructions: string;
    created_date?: string;
    modified_date?: string;
    created_by_email?: string;
    modified_by_email?: string;
  }