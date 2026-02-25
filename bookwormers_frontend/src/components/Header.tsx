import { BookOpen, Plus } from "lucide-react";
import { Button } from "@/components/ui/button";

interface HeaderProps {
  onAddBook: () => void;
}

export function Header({ onAddBook }: HeaderProps) {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto flex h-16 items-center justify-between px-4">
        <div className="flex items-center gap-3">
          <div className="flex items-center justify-center w-10 h-10 rounded-lg bg-primary text-primary-foreground">
            <BookOpen className="h-5 w-5" />
          </div>
          <div>
            <h1 className="font-serif text-xl font-bold text-foreground">
              Bookwormers
            </h1>
            <p className="text-xs text-muted-foreground">Your personal library</p>
          </div>
        </div>

        <Button onClick={onAddBook} className="gap-2">
          <Plus className="h-4 w-4" />
          Add Book
        </Button>
      </div>
    </header>
  );
}
