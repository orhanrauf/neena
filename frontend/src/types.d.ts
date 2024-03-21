export interface Dependency {
  instruction?: string; // Optional, with a maximum length of 512 characters
  flow: string; // UUID as a string
  source_task_operation: string; // UUID as a string
  target_task_operation: string; // UUID as a string
}

export interface Dependency {
  id?: string;
  flow?: string;
  source_drawflow_node_id: int;
  target_drawflow_node_id: int;
  instructions: string;
  created_date?: string;
  modified_date?: string; 
  created_by_email?: string;
  modified_by_email?: string;
}

  
export interface FlowRequest {
  id?: string;
  request_instructions: string;
  request_name?: string;
  request_metadata? : Array<Record<string, unknown>>;
  created_date?: string; // Optional
  modified_date?: string; // Optional
  created_by_email?: string; // Optional
  modified_by_email?: string; // Optional
}
enum FlowStatus {
  Pending = "Pending",
  Running = "Running", 
  Completed = "Completed",
  Failed = "Failed"
}

export interface FlowRun {
  id?: string; // Optional, UUID as a string
  flow: string; // UUID as a string
  status: FlowStatus;
  triggered_time?: Date | null; // Optional, represented as Date or null
  start_time?: Date | null; // Optional, represented as Date or null
  end_time?: Date | null; // Optional, represented as Date or null
  triggered_by?: string | null; // Optional, string
}


export interface Flow {
  name?: string | null; // Optional string
  task_operation? : TaskOperation[]; // Optional
  created_by_human?: boolean; // Optional
  modified_by_human?: boolean; // Optional
  id?: string; // UUID as a string, optional
  created_date?: Date; // Optional
  modified_date?: Date; // Optional
  created_by_email?: string; // Email as string, optional
  modified_by_email?: string; // Email as string, optional
  organization?: string | null; // Optional UUID as a string
}

export interface IntegrationCredential {
  credential: string; 
  integration: string;
  id?: string | null; // UUID as a string, optional
  created_by_email?: string; // Email as string, optional
  organization?: string | null; // UUID as a string, optional
  modified_by_email?: string; // Email as string, optional
  created_date?: Date; // Optional
  modified_date?: Date; // Optional
}

export interface Integration {
  id?: string | null; // UUID as a string, optional
  name: string; // Required
  short_name: string; // Required
  uses_api_key: boolean; // Required
  uses_sso_key: boolean; 
  created_date?: Date; // Required
  modified_date?: Date; // Required
}

export interface Task {
  id: number;
  task_name: string;
  iconUrl: string;
  task_description: string;
  output_type: string;
  source: string;
}


interface TaskParameter {
  name: string; // Corresponds to Python's str
  data_type: string; // Corresponds to Python's str
  position: number; // Corresponds to Python's int
  doc_string: string; // Corresponds to Python's str
  optional: boolean; // Corresponds to Python's bool
}


export interface TaskDefinition {
  id: string;
  task_name: string;
  integration: string;
  parameters: TaskParameter[];
  input_type: string;
  input_yml: string;
  description: string;
  python_method_name: string;
  output_type: string;
  output_yml: string;
  created_date: string;
  modified_date: string;
  created_by_email?: string;
  modified_by_email?: string;
  deleted_at?: string | null;
}

export interface TaskOperation {
  id?: string;
  drawflow_node_id?: int;
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

export interface TaskPrepAnswer {
  natural_language_explanation: string; 
  body: string; 
  has_python_execution: boolean; 
  task_prep_prompt_id: string;
  task_run_i?: string;
  id?: string | null; // UUID as a string, optional
  created_date?: Date; // Optional
}

export interface TaskPrepPrompt {
  body: string; 
  task_run_id: string;
  id?: string | null; // UUID as a string, optional
  created_date?: Date; // Optional
}

enum TaskStatus {
  Pending = "pending",
  InProgress = "in_progress",
  Completed = "completed",
  Failed = "failed",
  Cancelled = "cancelled"
}

interface TaskRunBase {
  task_operation_id: string;
  flow_run_id: string;
  status: TaskStatus;
  start_time: Date; // datetime in Python is represented as Date in TypeScript
  result: Record<string, any>; // dict in Python is similar to Record<string, any> in TypeScript
  end_time?: Date | null; // Optional datetime in Python is represented as Date | null in TypeScript
}

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: "bearer";
}

export interface User {
  email: string;
  auth0_id: string;
  full_name: string;
  id?: string;
  permissions?: string[];
}