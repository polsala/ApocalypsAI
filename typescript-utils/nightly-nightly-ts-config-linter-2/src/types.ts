export interface ConfigError {
  path: string;
  message: string;
}

export interface ConfigRule {
  path: string;
  description: string;
  validator: (value: any) => boolean;
}
