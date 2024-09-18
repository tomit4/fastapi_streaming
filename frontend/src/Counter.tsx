import { createSignal } from 'solid-js'
import type { Component } from 'solid-js'

const Counter: Component = () => {
    const [count, setCount] = createSignal(0)
    const increment = () => setCount(prev => prev + 1)

    return (
        <>
            <span>Count:: {count()}</span>{' '}
            <button type='button' onClick={increment}>
                Increment
            </button>
        </>
    )
}

export default Counter
