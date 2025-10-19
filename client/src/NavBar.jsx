import { useNavigate } from "react-router-dom";
import {
  NavigationMenu,
  NavigationMenuList,
  NavigationMenuItem,
  NavigationMenuLink,
  navigationMenuTriggerStyle,
} from "@/components/ui/navigation-menu";
import { Button } from "@/components/ui/button";

export default function NavBar() {
  const navigate = useNavigate();

  const handleHomeClick = () => {
    navigate("/");
  };

  return (
    <nav className="w-full bg-background border-b shadow-sm">
      <div className="flex items-center justify-between px-6 py-4">
        <h1
          onClick={handleHomeClick}
          className="text-2xl font-semibold tracking-tight text-foreground cursor-pointer hover:opacity-80 transition-opacity"
        >
          Lehigh Hacks
        </h1>

=        <NavigationMenu>
          <NavigationMenuList>
            <NavigationMenuItem>
              <NavigationMenuLink asChild>
                <Button
                  variant="secondary"
                  onClick={handleHomeClick}
                  className={navigationMenuTriggerStyle()}
                >
                  Home
                </Button>
              </NavigationMenuLink>
            </NavigationMenuItem>
          </NavigationMenuList>
        </NavigationMenu>
      </div>
    </nav>
  );
}


