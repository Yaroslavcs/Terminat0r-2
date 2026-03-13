import { useState, useRef, useEffect, useCallback } from "react";
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Animated,
} from "react-native";
import { router } from "expo-router";
import { CameraView, useCameraPermissions } from "expo-camera";
import { api } from "../services/api";

const CAPTURE_INTERVAL = 45000;

export default function Home() {
  const [permission, requestPermission] = useCameraPermissions();
  const [fact, setFact] = useState<string | null>(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [cameraOn, setCameraOn] = useState(true);
  const cameraRef = useRef<CameraView>(null);
  const fadeAnim = useRef(new Animated.Value(0)).current;

  const analyzingRef = useRef(false);

  const captureAndAnalyze = useCallback(async () => {
    if (!cameraRef.current || !permission?.granted || analyzingRef.current) return;
    analyzingRef.current = true;
    setAnalyzing(true);
    try {
      const photo = await cameraRef.current.takePictureAsync({
        base64: true,
        quality: 0.5,
      });
      if (photo?.base64) {
        const res = await api.analyzeScene(photo.base64);
        setFact(res.fact);
        fadeAnim.setValue(0);
        Animated.sequence([
          Animated.timing(fadeAnim, { toValue: 1, duration: 400, useNativeDriver: true }),
          Animated.delay(8000),
          Animated.timing(fadeAnim, { toValue: 0, duration: 400, useNativeDriver: true }),
        ]).start();
      }
    } catch {
      setFact("Щось пішло не так. Спробуй ще раз.");
    } finally {
      analyzingRef.current = false;
      setAnalyzing(false);
    }
  }, [permission?.granted, fadeAnim]);

  useEffect(() => {
    if (!permission?.granted || !cameraOn) return;
    const t1 = setTimeout(captureAndAnalyze, 3000);
    const id = setInterval(captureAndAnalyze, CAPTURE_INTERVAL);
    return () => {
      clearTimeout(t1);
      clearInterval(id);
    };
  }, [permission?.granted, cameraOn, captureAndAnalyze]);

  useEffect(() => {
    if (!permission?.granted && permission?.canAskAgain) {
      requestPermission();
    }
  }, [permission]);

  return (
    <View style={styles.container}>
      {cameraOn && permission?.granted ? (
        <CameraView style={styles.camera} ref={cameraRef}>
          <View style={styles.overlay}>
            <TouchableOpacity
              style={styles.toggleBtn}
              onPress={() => setCameraOn(false)}
            >
              <Text style={styles.toggleText}>приховати камеру</Text>
            </TouchableOpacity>
            {analyzing && (
              <View style={styles.analyzingBadge}>
                <Text style={styles.analyzingText}>аналіз...</Text>
              </View>
            )}
          </View>
        </CameraView>
      ) : (
        <View style={styles.placeholder}>
          <Text style={styles.placeholderText}>камера вимкнена</Text>
          <TouchableOpacity
            style={styles.toggleBtn}
            onPress={() => permission?.granted && setCameraOn(true)}
          >
            <Text style={styles.toggleText}>увімкнути камеру</Text>
          </TouchableOpacity>
        </View>
      )}

      {fact && (
        <Animated.View style={[styles.factCard, { opacity: fadeAnim }]}>
          <Text style={styles.factLabel}>цікавий факт</Text>
          <Text style={styles.factText}>{fact}</Text>
        </Animated.View>
      )}

      <View style={styles.footer}>
        <TouchableOpacity onPress={() => router.push("/quest-create")}>
          <Text style={styles.footerLink}>квести</Text>
        </TouchableOpacity>
        <TouchableOpacity onPress={() => router.push("/stats")}>
          <Text style={styles.footerLink}>статистика</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#0a0a12" },
  camera: { flex: 1 },
  placeholder: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#1a1a2e",
  },
  placeholderText: { color: "#666", fontSize: 16, marginBottom: 16 },
  overlay: {
    position: "absolute",
    top: 48,
    left: 0,
    right: 0,
    alignItems: "center",
  },
  toggleBtn: {
    backgroundColor: "rgba(0,0,0,0.6)",
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 8,
  },
  toggleText: { color: "#eaeaea", fontSize: 14 },
  analyzingBadge: {
    marginTop: 12,
    backgroundColor: "rgba(233,69,96,0.8)",
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 8,
  },
  analyzingText: { color: "#fff", fontSize: 14 },
  factCard: {
    position: "absolute",
    bottom: 100,
    left: 20,
    right: 20,
    backgroundColor: "rgba(26,33,62,0.95)",
    borderRadius: 16,
    padding: 20,
    borderWidth: 1,
    borderColor: "#0f3460",
  },
  factLabel: {
    fontSize: 12,
    color: "#e94560",
    marginBottom: 8,
    textTransform: "uppercase",
  },
  factText: { fontSize: 16, color: "#eaeaea", lineHeight: 24 },
  footer: {
    position: "absolute",
    bottom: 0,
    left: 0,
    right: 0,
    flexDirection: "row",
    justifyContent: "space-around",
    padding: 20,
    backgroundColor: "rgba(0,0,0,0.5)",
  },
  footerLink: { color: "#e94560", fontSize: 16 },
});
