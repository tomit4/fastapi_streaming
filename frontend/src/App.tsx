import { createSignal, For, onCleanup, onMount, Show } from "solid-js";
import type { Component } from "solid-js";

import styles from "./App.module.css";

const App: Component = () => {
    const [images, setImages] = createSignal<string[]>([]);
    const [loadingStates, setLoadingStates] = createSignal<boolean[]>([]);

    const abortController = new AbortController();

    const startStreaming = async () => {
        const response = await fetch("http://localhost:8000/users/streaming/", {
            signal: abortController.signal,
        });

        const reader = response.body!.getReader();

        const decoder = new TextDecoder();
        let done = false;
        let base64Chunk = "";

        while (!done) {
            const { value, done: readerDone } = await reader.read();
            done = readerDone;

            if (value) {
                base64Chunk += decoder.decode(value, { stream: true });
                if (base64Chunk.length) {
                    setImages(prev => [...prev, base64Chunk]);
                    setLoadingStates(prev => [...prev, false]);
                    base64Chunk = "";
                }
            }
        }
    };

    onMount(async () => {
        const response = await fetch(
            "http://localhost:8000/users/image-count/",
        );
        const { image_count } = await response.json();
        setLoadingStates(Array(image_count).fill(true));

        startStreaming();
    });

    const handleImageLoad = () => {
        setLoadingStates(prev => {
            const newState = [...prev];
            newState.shift();
            return newState;
        });
    };

    onCleanup(() => {
        abortController.abort();
        console.log("Cleanup: Stream aborted.");
    });

    return (
        <div class={styles.Gallery}>
            <Show when={images().length} fallback={<p>Loading...</p>}>
                <div class={styles["gallery"]}>
                    <For each={images()}>
                        {(image, index) => (
                            <>
                                <img
                                    src={`data:image/webp;base64,${image}`}
                                    alt={`Image ${index()}`}
                                    onLoad={() => handleImageLoad()}
                                />
                            </>
                        )}
                    </For>
                    <For each={loadingStates()}>
                        {(_, index) => (
                            <Show when={loadingStates()[index()]}>
                                <div class={styles["spinner"]}>
                                    <div></div>
                                    <div></div>
                                    <div></div>
                                    <div></div>
                                </div>
                            </Show>
                        )}
                    </For>
                </div>
            </Show>
        </div>
    );
};

export default App;
