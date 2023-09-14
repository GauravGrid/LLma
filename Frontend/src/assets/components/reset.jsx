import { useEffect } from "react";
import useAppStore from "./states";
import { useLocation } from "react-router-dom";

const ResetOnPageReload = () => {
    const location = useLocation();

    useEffect(() => {
      useAppStore.getState().resetState();
    }, [location]);
  

  return null;
};

export default ResetOnPageReload