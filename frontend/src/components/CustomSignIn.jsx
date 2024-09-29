import React from "react";
import { SignIn } from "@clerk/clerk-react";
import Navbar from "./Navbar";

const CustomSignIn = () => {
  return (
    <>
      <Navbar />

      <div className="signIn bg-white dark:bg-gray-900">
        <SignIn routing="path" path="/sign-in" />
      </div>
    </>
  );
};

export default CustomSignIn;
