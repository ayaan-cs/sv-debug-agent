export type Sample = {
  id: string;
  title: string;
  content: string;
};

export type AppStatus = {
  demo_mode: boolean;
  has_api_key: boolean;
  app_name: string;
};

export type Alternative = {
  title: string;
  code: string;
  note?: string;
};

export type DebugResponse = {
  result: string;
  demo_mode: boolean;
  alternatives?: Alternative[];
};
