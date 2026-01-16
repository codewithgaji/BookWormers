export type ReadingStatus = "want_to_read" | "reading" | "completed" | "dropped";

export interface Book {
  id: number;
  title: string;
  author: string;
  genre: string;
  status: ReadingStatus;
  description?: string;
  pages?: number;
  rating?: number;
  created_at?: string;
  updated_at?: string;
}

export interface BookCreate {
  title: string;
  author: string;
  genre: string;
  status: ReadingStatus;
  description?: string;
  pages?: number;
  rating?: number;
}

export interface BookUpdate {
  title?: string;
  author?: string;
  genre?: string;
  status?: ReadingStatus;
  description?: string;
  pages?: number;
  rating?: number;
}
