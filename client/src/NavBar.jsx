import { useNavigate } from "react-router-dom";
import {
  NavigationMenu,
  NavigationMenuList,
  NavigationMenuItem,
  NavigationMenuLink,
  navigationMenuTriggerStyle,
} from "@/components/ui/navigation-menu";
import { Button } from "@/components/ui/button";
import { Authenticator } from '@aws-amplify/ui-react';

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
          className="text-2xl font-semibold tracking-tight cusror-pointer text-foreground cursor-pointer hover:opacity-80 transition-opacity"
        >
          SelfQuest
        </h1>
        <p className="text-lg text-slate-600 hidden lg:block ">Therapy through Create-Your-Own-Adventure Storytelling</p>

        <NavigationMenu>
          <NavigationMenuList>
            <NavigationMenuItem>
              <NavigationMenuLink asChild>
                <Button
                  variant="secondary"
                  onClick={handleHomeClick}
                    className={`${navigationMenuTriggerStyle()} transition-all cusror-pointer hover:bg-black hover:text-white`}
                >
                  Home
                </Button>
              </NavigationMenuLink>
            </NavigationMenuItem>

            <NavigationMenuItem>
              <NavigationMenuLink asChild>
                <Authenticator>
                {({ signOut }) => (
                    <Button
                    variant="secondary"
                    onClick={signOut}
                    className={`${navigationMenuTriggerStyle()} transition-all cusror-pointer hover:bg-red-600 hover:text-white`}
                    >
                        Sign Out
                    </Button>
                )}
                </Authenticator>
              </NavigationMenuLink>
            </NavigationMenuItem>
          </NavigationMenuList>
        </NavigationMenu>
      </div>
    </nav>
  );
}