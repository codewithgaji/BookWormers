import { BookOpen, Plus } from "lucide-react";
import { Button } from "@/components/ui/button";

interface EmptyStateProps {
  onAddBook: () => void;
  hasFilters: boolean;
}

export function EmptyState({ onAddBook, hasFilters }: EmptyStateProps) {
  if (hasFilters) {
    return (
      <div className="flex flex-col items-center justify-center py-16 text-center">
        <div className="w-16 h-16 rounded-full bg-muted flex items-center justify-center mb-4">
          <BookOpen className="h-8 w-8 text-muted-foreground" />
        </div>
        <h3 className="font-serif text-xl font-semibold text-foreground mb-2">
          No books found
        </h3>
        <p className="text-muted-foreground max-w-sm">
          Try adjusting your search or filter criteria to find what you're looking for.
        </p>
      </div>
    );
  }

  return (
    <div className="flex flex-col items-center justify-center py-16 text-center">
      <div className="w-20 h-20 rounded-full bg-primary/10 flex items-center justify-center mb-6">
        <BookOpen className="h-10 w-10 text-primary" />
      </div>
      <h3 className="font-serif text-2xl font-semibold text-foreground mb-2">
        Your library is empty
      </h3>
      <p className="text-muted-foreground max-w-sm mb-6">
        Start building your personal collection by adding your first book.
      </p>
      <Button onClick={onAddBook} className="gap-2">
        <Plus className="h-4 w-4" />
        Add Your First Book
      </Button>
    </div>
  );
}
