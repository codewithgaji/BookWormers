import { Search } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { ReadingStatus } from "@/types/book";

interface FilterBarProps {
  search: string;
  onSearchChange: (value: string) => void;
  activeFilter: ReadingStatus | "all";
  onFilterChange: (filter: ReadingStatus | "all") => void;
}

const filters: { value: ReadingStatus | "all"; label: string }[] = [
  { value: "all", label: "All" },
  { value: "reading", label: "Reading" },
  { value: "want_to_read", label: "Want to Read" },
  { value: "completed", label: "Completed" },
  { value: "dropped", label: "Dropped" },
];

export function FilterBar({
  search,
  onSearchChange,
  activeFilter,
  onFilterChange,
}: FilterBarProps) {
  return (
    <div className="flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
      <div className="relative w-full sm:w-80">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
        <Input
          placeholder="Search books by title or author..."
          value={search}
          onChange={(e) => onSearchChange(e.target.value)}
          className="pl-10"
        />
      </div>

      <div className="flex gap-2 flex-wrap">
        {filters.map((filter) => (
          <Button
            key={filter.value}
            variant={activeFilter === filter.value ? "default" : "outline"}
            size="sm"
            onClick={() => onFilterChange(filter.value)}
            className="text-xs"
          >
            {filter.label}
          </Button>
        ))}
      </div>
    </div>
  );
}
