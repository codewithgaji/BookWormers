import { Book, ReadingStatus } from "@/types/book";
import { Card, CardContent, CardFooter, CardHeader } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Pencil, Trash2, Star, BookOpen } from "lucide-react";

interface BookCardProps {
  book: Book;
  onEdit: (book: Book) => void;
  onDelete: (id: number) => void;
}

const statusConfig: Record<ReadingStatus, { label: string; className: string }> = {
  want_to_read: { label: "Want to Read", className: "bg-status-want text-white" },
  reading: { label: "Reading", className: "bg-status-reading text-white" },
  completed: { label: "Completed", className: "bg-status-completed text-white" },
  dropped: { label: "Dropped", className: "bg-status-dropped text-white" },
};

const genreColors: Record<string, string> = {
  fiction: "bg-amber-100 text-amber-800 dark:bg-amber-900 dark:text-amber-100",
  "non-fiction": "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100",
  mystery: "bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-100",
  fantasy: "bg-indigo-100 text-indigo-800 dark:bg-indigo-900 dark:text-indigo-100",
  romance: "bg-pink-100 text-pink-800 dark:bg-pink-900 dark:text-pink-100",
  thriller: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100",
  "sci-fi": "bg-cyan-100 text-cyan-800 dark:bg-cyan-900 dark:text-cyan-100",
  biography: "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100",
};

export function BookCard({ book, onEdit, onDelete }: BookCardProps) {
  const status = statusConfig[book.status];
  const genreColor = genreColors[book.genre.toLowerCase()] || "bg-secondary text-secondary-foreground";

  return (
    <Card className="group relative overflow-hidden transition-all duration-300 hover:shadow-lg hover:-translate-y-1 border-border/50">
      <div className="absolute top-0 left-0 w-1 h-full bg-primary opacity-0 group-hover:opacity-100 transition-opacity" />
      
      <CardHeader className="pb-2">
        <div className="flex items-start justify-between gap-2">
          <div className="flex-1 min-w-0">
            <h3 className="font-serif font-bold text-lg leading-tight text-foreground truncate">
              {book.title}
            </h3>
            <p className="text-muted-foreground text-sm mt-1">by {book.author}</p>
          </div>
          <Badge className={status.className}>{status.label}</Badge>
        </div>
      </CardHeader>

      <CardContent className="pb-3">
        <div className="flex items-center gap-2 flex-wrap">
          <Badge variant="outline" className={genreColor}>
            {book.genre}
          </Badge>
          {book.pages && (
            <span className="text-xs text-muted-foreground flex items-center gap-1">
              <BookOpen className="h-3 w-3" />
              {book.pages} pages
            </span>
          )}
        </div>
        
        {book.rating && (
          <div className="flex items-center gap-1 mt-2">
            {Array.from({ length: 5 }).map((_, i) => (
              <Star
                key={i}
                className={`h-4 w-4 ${
                  i < book.rating! ? "fill-accent text-accent" : "text-muted"
                }`}
              />
            ))}
          </div>
        )}

        {book.description && (
          <p className="text-sm text-muted-foreground mt-3 line-clamp-2">
            {book.description}
          </p>
        )}
      </CardContent>

      <CardFooter className="pt-0 gap-2">
        <Button
          variant="ghost"
          size="sm"
          onClick={() => onEdit(book)}
          className="flex-1"
        >
          <Pencil className="h-4 w-4 mr-1" />
          Edit
        </Button>
        <Button
          variant="ghost"
          size="sm"
          onClick={() => onDelete(book.id)}
          className="flex-1 text-destructive hover:text-destructive hover:bg-destructive/10"
        >
          <Trash2 className="h-4 w-4 mr-1" />
          Delete
        </Button>
      </CardFooter>
    </Card>
  );
}
