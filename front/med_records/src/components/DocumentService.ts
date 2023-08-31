import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/';

export interface Document {
  id: number;
  date: string;
  source_doc_url: string;
  user_id: number;
  physician_id: number | null;
  hospital_id: number | null;
  condition_id: number | null;
  treatment_id: number | null;
}

export async function createDocument(
  formData: FormData
): Promise<Document> {
  const response = await axios.post<Document>(
    `${API_BASE_URL}/documents/`,
    formData,
    {
      headers: { 'Content-Type': 'multipart/form-data' }
    }
  );
  return response.data;
}

export async function getDocumentById(id: number): Promise<Document> {
  const response = await axios.get<Document>(
    `${API_BASE_URL}/documents/${id}`
  );
  return response.data;
}

export async function updateDocument(
  id: number,
  document: Document
): Promise<Document> {
  const response = await axios.put<Document>(
    `${API_BASE_URL}/documents/${id}/`,
    document
  );
  return response.data;
}

export async function deleteDocument(id: number): Promise<void> {
  await axios.delete(`${API_BASE_URL}/documents/${id}/`);
}
