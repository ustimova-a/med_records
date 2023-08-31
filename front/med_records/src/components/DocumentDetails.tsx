import React, { useEffect, useState } from 'react';
import { Document, getDocumentById } from './DocumentService';

interface DocumentDetailsProps {
  documentId: number;
}

const DocumentDetails: React.FC<DocumentDetailsProps> = ({ documentId }) => {
  const [document, setDocument] = useState<Document | null>(null);

  useEffect(() => {
    async function fetchDocument() {
      try {
        const fetchedDocument = await getDocumentById(documentId);
        setDocument(fetchedDocument);
      } catch (error) {
        // Handle error
      }
    }

    fetchDocument();
  }, [documentId]);

  if (!document) {
    // Loading indicator or error message
    return null;
  }

  return (
    <div>
      <h2>Document Details</h2>
      <p>ID: {document.id}</p>
      <p>Date: {document.date}</p>
      {/* Display other document details */}
      <p>Physician: {document.physician_id}</p>
      {/* Display other related fields */}
    </div>
  );
};

export default DocumentDetails;
