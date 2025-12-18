import { createAuthClient } from "better-auth/react";
import { atom, useAtom } from "jotai";

export const authClient = createAuthClient({
  baseURL: process.env.REACT_APP_BACKEND_URL || "http://localhost:8000",
  fetchOptions: {
    cache: "no-store",
  },
});

// Jotai atoms for auth state management
export const userAtom = atom(null);
export const isSignedInAtom = atom(false);

// Custom hook for auth state
export const useAuth = () => {
  const [user, setUser] = useAtom(userAtom);
  const [isSignedIn, setIsSignedIn] = useAtom(isSignedInAtom);

  const signIn = async (email, password) => {
    try {
      const response = await authClient.signIn.email({
        email,
        password,
        callbackURL: "/",
      });
      if (response.data) {
        setUser(response.data.user);
        setIsSignedIn(true);
        return { success: true, user: response.data.user };
      }
      return { success: false, error: response.error };
    } catch (error) {
      return { success: false, error: error.message };
    }
  };

  const signUp = async (email, password, name, backgroundData = {}) => {
    try {
      const response = await authClient.signUp.email({
        email,
        password,
        name,
        ...backgroundData, // Include user background information
      });
      if (response.data) {
        setUser(response.data.user);
        setIsSignedIn(true);
        return { success: true, user: response.data.user };
      }
      return { success: false, error: response.error };
    } catch (error) {
      return { success: false, error: error.message };
    }
  };

  const signOut = async () => {
    try {
      await authClient.signOut();
      setUser(null);
      setIsSignedIn(false);
    } catch (error) {
      console.error("Sign out error:", error);
    }
  };

  return {
    user,
    isSignedIn,
    signIn,
    signUp,
    signOut,
  };
};