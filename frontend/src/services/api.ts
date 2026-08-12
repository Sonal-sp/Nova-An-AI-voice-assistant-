import axios from 'axios';

const API_BASE_URL = '/api';

export const api = axios.create({
  baseURL: API_BASE_URL,
});

export interface Message {
  role: 'user' | 'assistant';
  content: string;
  citations?: any[];
  metadata?: any;
}

export const fetchHealth = async () => {
  const res = await api.get('/health');
  return res.data;
};

export const fetchModels = async () => {
  const res = await api.get('/models');
  return res.data;
};

export const fetchNotes = async (query = '') => {
  const res = await api.get(`/notes?query=${encodeURIComponent(query)}`);
  return res.data.notes;
};

export const createNote = async (title: string, content: string, tags = '') => {
  const res = await api.post('/notes', { title, content, tags });
  return res.data;
};

export const deleteNote = async (id: number) => {
  const res = await api.delete(`/notes/${id}`);
  return res.data;
};

export const fetchTodos = async (statusFilter = 'all') => {
  const res = await api.get(`/todos?status_filter=${statusFilter}`);
  return res.data.todos;
};

export const createTodo = async (task: string, dueDate = '', priority = 'Medium') => {
  const res = await api.post('/todos', { task, due_date: dueDate, priority });
  return res.data;
};

export const toggleTodo = async (id: number) => {
  const res = await api.put(`/todos/${id}/toggle`);
  return res.data;
};

export const deleteTodo = async (id: number) => {
  const res = await api.delete(`/todos/${id}`);
  return res.data;
};

export const fetchAgenda = async () => {
  const res = await api.get('/agenda');
  return res.data;
};

export const fetchIntegrations = async () => {
  const res = await api.get('/integrations');
  return res.data;
};

export const launchDesktopApp = async (appName: string) => {
  const res = await api.post('/launch-app', { app_name: appName });
  return res.data;
};

export const fetchDiagnostics = async () => {
  const res = await api.get('/diagnostics');
  return res.data;
};

export const uploadPdfDocument = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  const res = await api.post('/upload-pdf', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return res.data;
};

export const analyzeVisionImage = async (file: File, prompt = '') => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('prompt', prompt);
  const res = await api.post('/vision', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return res.data;
};

export const fetchSettings = async () => {
  const res = await api.get('/settings');
  return res.data;
};

export const saveSettings = async (settings: any) => {
  const res = await api.post('/settings', { settings });
  return res.data;
};

export const clearMessages = async () => {
  const res = await api.delete('/messages');
  return res.data;
};
