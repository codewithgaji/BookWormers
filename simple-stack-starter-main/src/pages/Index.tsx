import { useState } from "react";
import { Book, BookCreate } from "@/types/book";
import { useBooks } from "@/hooks/useBooks";
import { Header } from "@/components/Header";
import { FilterBar } from "@/components/FilterBar";
import { BookCard } from "@/components/BookCard";
import { BookForm } from "@/components/BookForm";
import { EmptyState } from "@/components/EmptyState";
import { DeleteConfirmDialog } from "@/components/DeleteConfirmDialog";
import { Skeleton } from "@/components/ui/skeleton";

const Index = () => {
  const {
    books,
    isLoading,
    search,
    setSearch,
    filter,
    setFilter,
    addBook,
    editBook,
    removeBook,
  } = useBooks();

  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingBook, setEditingBook] = useState<Book | null>(null);
  const [deletingBook, setDeletingBook] = useState<Book | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleAddBook = () => {
    setEditingBook(null);
    setIsFormOpen(true);
  };

  const handleEditBook = (book: Book) => {
    setEditingBook(book);
    setIsFormOpen(true);
  };

  const handleDeleteClick = (id: number) => {
    const book = books.find((b) => b.id === id);
    if (book) {
      setDeletingBook(book);
    }
  };

  const handleFormSubmit = async (data: BookCreate) => {
    setIsSubmitting(true);
    try {
      if (editingBook) {
        await editBook(editingBook.id, data);
      } else {
        await addBook(data);
      }
      setIsFormOpen(false);
      setEditingBook(null);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDeleteConfirm = async () => {
    if (!deletingBook) return;
    setIsSubmitting(true);
    try {
      await removeBook(deletingBook.id);
      setDeletingBook(null);
    } finally {
      setIsSubmitting(false);
    }
  };

  const hasFilters = search !== "" || filter !== "all";

  return (
    <div className="min-h-screen bg-background">
      <Header onAddBook={handleAddBook} />

      <main className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h2 className="font-serif text-3xl font-bold text-foreground mb-2">
            My Library
          </h2>
          <p className="text-muted-foreground">
            Track and manage your reading journey
          </p>
        </div>

        <div className="mb-6">
          <FilterBar
            search={search}
            onSearchChange={setSearch}
            activeFilter={filter}
            onFilterChange={setFilter}
          />
        </div>

        {isLoading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {Array.from({ length: 8 }).map((_, i) => (
              <div key={i} className="space-y-3">
                <Skeleton className="h-48 w-full rounded-lg" />
              </div>
            ))}
          </div>
        ) : books.length === 0 ? (
          <EmptyState onAddBook={handleAddBook} hasFilters={hasFilters} />
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {books.map((book) => (
              <BookCard
                key={book.id}
                book={book}
                onEdit={handleEditBook}
                onDelete={handleDeleteClick}
              />
            ))}
          </div>
        )}
      </main>

      <BookForm
        open={isFormOpen}
        onOpenChange={setIsFormOpen}
        onSubmit={handleFormSubmit}
        initialData={editingBook}
        isLoading={isSubmitting}
      />

      <DeleteConfirmDialog
        open={!!deletingBook}
        onOpenChange={(open) => !open && setDeletingBook(null)}
        onConfirm={handleDeleteConfirm}
        bookTitle={deletingBook?.title}
        isLoading={isSubmitting}
      />
    </div>
  );
};

export default Index;
