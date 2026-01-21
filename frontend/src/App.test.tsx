import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import App from './App'

describe('App', () => {
    it('отображает страницу авторизации для неавторизованных', () => {
        render(<App />)
        expect(screen.getByText('Messenger')).toBeInTheDocument()
    })
})
