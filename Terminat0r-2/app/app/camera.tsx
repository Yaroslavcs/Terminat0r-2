import { useState, useRef, useEffect } from "react";
import { View, Text, TouchableOpacity, StyleSheet, Alert } from "react-native";
import { router, useLocalSearchParams } from "expo-router";
import { CameraView, useCameraPermissions } from "expo-camera";
import { useDeviceId } from "../hooks/useDeviceId";
import { api } from "../services/api";

export default function CameraScreen() {
  const { questId } = useLocalSearchParams<{ questId: string }>();
  const [permission, requestPermission] = useCameraPermissions();
  const [capturing, setCapturing] = useState(false);
  const cameraRef = useRef<CameraView>(null);

  const deviceId = useDeviceId();

  useEffect(() => {
    if (!permission?.granted && permission?.canAskAgain) {
      requestPermission();
    }
  }, [permission]);

  async function capture() {
    if (!cameraRef.current || !questId || !permission?.granted) return;
    setCapturing(true);
    try {
      const photo = await cameraRef.current.takePictureAsync({
        base64: true,
        quality: 0.7,
      });
      const imageB64 = photo?.base64;
      const res = await api.verifyQuest(
        deviceId,
        parseInt(questId, 10),
        imageB64
      );
      Alert.alert(
        res.verified ? "Quest complete!" : "Partial success",
        `${res.message}\n+${res.gold_earned} gold, +${res.xp_earned} xp`,
        [{ text: "OK", onPress: () => router.replace("/") }]
      );
    } catch (e) {
      Alert.alert("Error", String(e));
    } finally {
      setCapturing(false);
    }
  }

  if (!permission) {
    return (
      <View style={styles.center}>
        <Text style={styles.text}>requesting camera...</Text>
      </View>
    );
  }

  if (!permission.granted) {
    return (
      <View style={styles.center}>
        <Text style={styles.text}>camera permission required</Text>
        <TouchableOpacity style={styles.btn} onPress={requestPermission}>
          <Text style={styles.btnText}>allow</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <CameraView style={styles.camera} ref={cameraRef}>
        <View style={styles.overlay}>
          <TouchableOpacity
            style={[styles.captureBtn, capturing && styles.captureDisabled]}
            onPress={capture}
            disabled={capturing}
          >
            <Text style={styles.captureText}>
              {capturing ? "verifying..." : "capture"}
            </Text>
          </TouchableOpacity>
        </View>
      </CameraView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#000" },
  camera: { flex: 1 },
  overlay: {
    flex: 1,
    justifyContent: "flex-end",
    alignItems: "center",
    paddingBottom: 48,
  },
  captureBtn: {
    backgroundColor: "#e94560",
    paddingHorizontal: 48,
    paddingVertical: 16,
    borderRadius: 12,
  },
  captureDisabled: { opacity: 0.6 },
  captureText: { color: "#fff", fontSize: 18, fontWeight: "600" },
  center: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#1a1a2e",
  },
  text: { color: "#eaeaea", fontSize: 16, marginBottom: 24 },
  btn: { backgroundColor: "#e94560", padding: 16, borderRadius: 12 },
  btnText: { color: "#fff", fontWeight: "600" },
});
