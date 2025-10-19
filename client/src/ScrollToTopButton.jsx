import { Button } from '@/components/ui/button';
import { ArrowUp } from 'lucide-react';

export default function ScrollToTopButton() {
      function scrollToTop() {
          window.scrollTo({
            top: 0,
            behavior: 'smooth'
          });
      }

      return(
        
        <Button
          onClick={scrollToTop}
          className="fixed bottom-8 right-8 bg-black hover:bg-amber-500 text-white p-3 rounded-full
                    transform transition duration-300 ease-in-out
                    hover:scale-110 hover:shadow-lg
                    active:scale-95 cursor-pointer z-50"
          aria-label="Scroll to top"
        >
          <ArrowUp size={24} />
        </Button>
      )
}