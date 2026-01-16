import { Book, BookCreate, BookUpdate } from "@/types/book";

// Configure your FastAPI backend URL here
const API_BASE_URL = "http://localhost:8000";

/**
 * GET /books
 * Fetches all books from the database
 * Used in: BookList component to display all books
 */
export async function getBooks(): Promise<Book[]> {
  const response = await fetch(`${API_BASE_URL}/books`);
  if (!response.ok) {
    throw new Error("Failed to fetch books");
  }
  return response.json();
}

/**
 * GET /books/{id}
 * Fetches a single book by ID
 * Used in: BookDetails modal/page
 */
export async function getBook(id: number): Promise<Book> {
  const response = await fetch(`${API_BASE_URL}/books/${id}`);
  if (!response.ok) {
    throw new Error("Failed to fetch book");
  }
  return response.json();
}

/**
 * POST /books
 * Creates a new book
 * Used in: AddBookForm component
 */
export async function createBook(book: BookCreate): Promise<Book> {
  const response = await fetch(`${API_BASE_URL}/books`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(book),
  });
  if (!response.ok) {
    throw new Error("Failed to create book");
  }
  return response.json();
}

/**
 * PUT /books/{id}
 * Updates an existing book
 * Used in: EditBookForm component
 */
export async function updateBook(id: number, book: BookUpdate): Promise<Book> {
  const response = await fetch(`${API_BASE_URL}/books/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(book),
  });
  if (!response.ok) {
    throw new Error("Failed to update book");
  }
  return response.json();
}

/**
 * DELETE /books/{id}
 * Deletes a book by ID
 * Used in: BookCard delete button
 */
export async function deleteBook(id: number): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/books/${id}`, {
    method: "DELETE",
  });
  if (!response.ok) {
    throw new Error("Failed to delete book");
  }
}
