import React, { useState } from 'react';
import { Document, createDocument } from './DocumentService.ts';

interface DocumentFormProps {
  onSuccess: () => void;
}

const DocumentForm: React.FC<DocumentFormProps> = ({ onSuccess }) => {
  const [file, setFile] = useState<File | null>(null);
  const [date, setDate] = useState<string>('');
  // Other form fields (physician, hospital, condition, treatment)

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      setFile(event.target.files[0]);
    }
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    if (!file) {
      // Handle file not selected error
      return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('file_date', date);
    // Append other form fields to formData

    try {
      await createDocument(formData);
      onSuccess();
    } catch (error) {
      // Handle error
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="file"
        accept=".pdf, .jpg, .png"
        onChange={handleFileChange}
      />
      <input
        type="text"
        placeholder="Date (dd.mm.yyyy)"
        value={date}
        onChange={(e) => setDate(e.target.value)}
      />
      {/* Other form inputs for physician, hospital, condition, treatment */}
      <select
        value={physicianId}
        onChange={(e) => setPhysicianId(Number(e.target.value))}
      >
        <option value={-1}>Select Physician</option>
        {/* Map over physicians and create options */}
      </select>
      <button type="submit">Upload Document</button>
    </form>
  );
};

export default DocumentForm;
