import React from 'react'
import {useState} from 'react'
import {Stack, TextField, Button } from '@mui/material'

function SignUp() {
  const [value, setValue] = useState("")
  return (
    <Stack spacing={4}>
        <Stack direction="row" spacing={2}>
            <TextField label="user-name" 
            required
            value={value}
            onChange={event => setValue(event.target.value)}
            error={!value}
            helperText={value? 'Required': 'user-name is required'}/>
        </Stack>
        <Stack direction="row" spacing={2}>
            <TextField label="email" required/>
        </Stack>
        <Stack direction="row" spacing={2}>
            <TextField 
            label="password"
            required
            type="password"
            helperText="Do not share your password with anyone"/>
        </Stack>
        <Stack direction="row" spacing={2}>
            <Button variant='contained'>Sign Up</Button>
        </Stack>
    </Stack>
  )
}

export default SignUp