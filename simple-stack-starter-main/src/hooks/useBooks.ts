import { useState, useEffect, useMemo } from "react";
import { Book, BookCreate, BookUpdate, ReadingStatus } from "@/types/book";
import { getBooks, createBook, updateBook, deleteBook } from "@/services/api";
import { toast } from "@/hooks/use-toast";

// Mock data for development when FastAPI is not running
const mockBooks: Book[] = [
  {
    id: 1,
    title: "The Great Gatsby",
    author: "F. Scott Fitzgerald",
    genre: "Fiction",
    status: "completed",
    pages: 180,
    rating: 5,
    description: "A story of the mysteriously wealthy Jay Gatsby and his love for Daisy Buchanan.",
  },
  {
    id: 2,
    title: "Atomic Habits",
    author: "James Clear",
    genre: "Self-Help",
    status: "reading",
    pages: 320,
    rating: 4,
    description: "An easy and proven way to build good habits and break bad ones.",
  },
  {
    id: 3,
    title: "Dune",
    author: "Frank Herbert",
    genre: "Sci-Fi",
    status: "want_to_read",
    pages: 688,
    description: "A science fiction masterpiece about politics, religion, and ecology on a desert planet.",
  },
  {
    id: 4,
    title: "The Hobbit",
    author: "J.R.R. Tolkien",
    genre: "Fantasy",
    status: "completed",
    pages: 310,
    rating: 5,
    description: "Bilbo Baggins embarks on an unexpected adventure with a group of dwarves.",
  },
];

// Set to true to use mock data (when FastAPI is not running)
const USE_MOCK_DATA = false;

export function useBooks() {
  const [books, setBooks] = useState<Book[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState("");
  const [filter, setFilter] = useState<ReadingStatus | "all">("all");

  // Fetch books on mount
  useEffect(() => {
    fetchBooks();
  }, []);

 const fetchBooks = async () => {
  setIsLoading(true);
  setError(null);

  try {
    const data = await getBooks();
    // SAFETY CHECK: If data is a string or null, set an empty array instead
    setBooks(Array.isArray(data) ? data : []); 
  } catch (err) {
    console.error("Fetch Error:", err);
    setError("Failed to fetch books.");
    setBooks([]); // Fallback to empty list so the UI doesn't crash
  } finally {
    setIsLoading(false);
  }
};

  const addBook = async (bookData: BookCreate) => {
    if (USE_MOCK_DATA) {
      const newBook: Book = {
        id: Math.max(...books.map((b) => b.id), 0) + 1,
        ...bookData,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      };
      setBooks((prev) => [...prev, newBook]);
      toast({ title: "Success", description: "Book added successfully!" });
      return newBook;
    }

    try {
      const newBook = await createBook(bookData);
      setBooks((prev) => [...prev, newBook]);
      toast({ title: "Success", description: "Book added successfully!" });
      return newBook;
    } catch (err) {
      toast({
        title: "Error",
        description: "Failed to add book",
        variant: "destructive",
      });
      throw err;
    }
  };

  const editBook = async (id: number, bookData: BookUpdate) => {
    if (USE_MOCK_DATA) {
      setBooks((prev) =>
        prev.map((book) =>
          book.id === id ? { ...book, ...bookData, updated_at: new Date().toISOString() } : book
        )
      );
      toast({ title: "Success", description: "Book updated successfully!" });
      return;
    }

    try {
      const updatedBook = await updateBook(id, bookData);
      setBooks((prev) =>
        prev.map((book) => (book.id === id ? updatedBook : book))
      );
      toast({ title: "Success", description: "Book updated successfully!" });
    } catch (err) {
      toast({
        title: "Error",
        description: "Failed to update book",
        variant: "destructive",
      });
      throw err;
    }
  };

  const removeBook = async (id: number) => {
    if (USE_MOCK_DATA) {
      setBooks((prev) => prev.filter((book) => book.id !== id));
      toast({ title: "Success", description: "Book deleted successfully!" });
      return;
    }

    try {
      await deleteBook(id);
      setBooks((prev) => prev.filter((book) => book.id !== id));
      toast({ title: "Success", description: "Book deleted successfully!" });
    } catch (err) {
      toast({
        title: "Error",
        description: "Failed to delete book",
        variant: "destructive",
      });
      throw err;
    }
  };

  // Filtered and searched books
  const filteredBooks = useMemo(() => {
    return books.filter((book) => {
      const matchesSearch =
        search === "" ||
        book.title.toLowerCase().includes(search.toLowerCase()) ||
        book.author.toLowerCase().includes(search.toLowerCase());
      const matchesFilter = filter === "all" || book.status === filter;
      return matchesSearch && matchesFilter;
    });
  }, [books, search, filter]);

  return {
    books: filteredBooks,
    allBooks: books,
    isLoading,
    error,
    search,
    setSearch,
    filter,
    setFilter,
    addBook,
    editBook,
    removeBook,
    refetch: fetchBooks,
  };
}
