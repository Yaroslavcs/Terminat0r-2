import { useState, useEffect } from "react";
import * as Application from "expo-application";
import { Platform } from "react-native";

export function useDeviceId(): string {
  const [id, setId] = useState("web-device");

  useEffect(() => {
    (async () => {
      if (Platform.OS === "android") {
        setId(Application.androidId || "android-device");
      } else if (Platform.OS === "ios") {
        const iosId = await Application.getIosIdForVendorAsync();
        setId(iosId || "ios-device");
      }
    })();
  }, []);

  return id;
}
