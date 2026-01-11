'use client';
import { useState, useRef, useEffect } from 'react';
import { Upload, FileText, CheckCircle, AlertCircle, Loader2, X } from 'lucide-react';

export function PDFUploader({ onExtractionComplete }) {
    const [isDragging, setIsDragging] = useState(false);
    const [isUploading, setIsUploading] = useState(false);
    const [uploadStatus, setUploadStatus] = useState(null);
    const [errorMessage, setErrorMessage] = useState(null);
    const fileInputRef = useRef(null);

    // Reset status after 3 seconds of success
    useEffect(() => {
        if (uploadStatus === 'success') {
            const timer = setTimeout(() => {
                setUploadStatus(null);
                setErrorMessage(null);
                // Reset file input
                if (fileInputRef.current) {
                    fileInputRef.current.value = '';
                }
            }, 3000);
            return () => clearTimeout(timer);
        }
    }, [uploadStatus]);

    const handleDrag = (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === 'dragenter' || e.type === 'dragover') {
            setIsDragging(true);
        } else if (e.type === 'dragleave') {
            setIsDragging(false);
        }
    };

    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragging(false);
        setErrorMessage(null);
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFiles(e.dataTransfer.files[0]);
        }
    };

    const handleChange = (e) => {
        e.preventDefault();
        setErrorMessage(null);
        if (e.target.files && e.target.files[0]) {
            handleFiles(e.target.files[0]);
        }
    };

    const handleFiles = async (file) => {
        // Reset previous errors
        setErrorMessage(null);

        // Validate file type
        if (file.type !== 'application/pdf') {
            setUploadStatus('error');
            setErrorMessage('Please upload a PDF file only');
            // Reset file input
            if (fileInputRef.current) {
                fileInputRef.current.value = '';
            }
            return;
        }

        // Validate file size (e.g., max 10MB)
        const maxSize = 10 * 1024 * 1024; // 10MB
        if (file.size > maxSize) {
            setUploadStatus('error');
            setErrorMessage('File size too large. Maximum size is 10MB');
            if (fileInputRef.current) {
                fileInputRef.current.value = '';
            }
            return;
        }

        setIsUploading(true);
        setUploadStatus(null);

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/api/process-pdf', {
                method: 'POST',
                body: formData,
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || data.details || 'Upload failed');
            }

            // Check if result is valid
            if (!data || !data.product_name) {
                throw new Error('Failed to extract data from PDF');
            }

            setUploadStatus('success');
            if (onExtractionComplete) onExtractionComplete(data);
            
            // Reset file input after successful upload
            if (fileInputRef.current) {
                fileInputRef.current.value = '';
            }
        } catch (error) {
            console.error('Upload error:', error);
            setUploadStatus('error');
            setErrorMessage(error.message || 'Failed to process PDF. Please try again.');
            // Reset file input on error
            if (fileInputRef.current) {
                fileInputRef.current.value = '';
            }
        } finally {
            setIsUploading(false);
        }
    };

    const handleReset = () => {
        setUploadStatus(null);
        setErrorMessage(null);
        if (fileInputRef.current) {
            fileInputRef.current.value = '';
        }
    };

    return (
        <div
            className="card"
            style={{
                border: isDragging ? '2px dashed #818cf8' : '2px dashed rgba(255,255,255,0.1)',
                background: isDragging ? 'rgba(129, 140, 248, 0.1)' : 'rgba(255,255,255,0.05)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                minHeight: '200px',
                cursor: 'pointer',
                position: 'relative'
            }}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
        >
            <input
                ref={fileInputRef}
                type="file"
                style={{ position: 'absolute', inset: 0, opacity: 0, width: '100%', height: '100%', cursor: isUploading ? 'not-allowed' : 'pointer' }}
                accept=".pdf,application/pdf"
                onChange={handleChange}
                disabled={isUploading}
            />

            <div className="flex-col items-center justify-center text-center" style={{ display: 'flex', gap: '1rem', position: 'relative', zIndex: 1 }}>
                {isUploading ? (
                    <>
                        <Loader2 size={40} className="text-primary animate-spin" style={{ color: '#818cf8', animation: 'spin 1s linear infinite' }} />
                        <div>
                            <p className="font-bold text-white">Analyzing Contract...</p>
                            <p className="text-sm text-muted">Extracting financial promises via OCR</p>
                        </div>
                    </>
                ) : uploadStatus === 'success' ? (
                    <>
                        <div style={{ width: '48px', height: '48px', background: 'rgba(16, 185, 129, 0.15)', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#34d399' }}>
                            <CheckCircle size={24} />
                        </div>
                        <div>
                            <p className="font-bold text-white">Analysis Complete</p>
                            <p className="text-sm text-muted">Ready for next document</p>
                        </div>
                        <button
                            onClick={handleReset}
                            className="btn btn-secondary"
                            style={{ marginTop: '0.5rem', padding: '0.25rem 0.75rem', fontSize: '0.75rem' }}
                        >
                            Upload Another
                        </button>
                    </>
                ) : uploadStatus === 'error' ? (
                    <>
                        <div style={{ width: '48px', height: '48px', background: 'rgba(248, 113, 113, 0.15)', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#f87171' }}>
                            <AlertCircle size={24} />
                        </div>
                        <div>
                            <p className="font-bold text-white">Upload Failed</p>
                            {errorMessage && (
                                <p className="text-sm text-red-300" style={{ marginTop: '0.25rem', maxWidth: '300px' }}>
                                    {errorMessage}
                                </p>
                            )}
                        </div>
                        <button
                            onClick={handleReset}
                            className="btn btn-secondary"
                            style={{ marginTop: '0.5rem', padding: '0.25rem 0.75rem', fontSize: '0.75rem' }}
                        >
                            Try Again
                        </button>
                    </>
                ) : (
                    <>
                        <div style={{ width: '48px', height: '48px', borderRadius: '50%', background: isDragging ? '#818cf8' : 'rgba(255,255,255,0.1)', color: isDragging ? 'white' : '#a1a1aa', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                            <Upload size={24} />
                        </div>
                        <div>
                            <p className="text-lg font-bold text-white">Drop product PDF here</p>
                            <p className="text-sm text-muted" style={{ maxWidth: '250px' }}>
                                Automatically extracts APY, Tenure, and Risk terms.
                            </p>
                            <p className="text-xs text-muted" style={{ marginTop: '0.25rem' }}>
                                Or click to browse (Max 10MB)
                            </p>
                        </div>
                    </>
                )}
            </div>
            <style jsx>{`
                @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
            `}</style>
        </div>
    );
}
