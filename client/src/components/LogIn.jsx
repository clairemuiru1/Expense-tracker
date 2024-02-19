import React from 'react'
import {useState} from 'react'
import {Stack, TextField, Button } from '@mui/material'
import LoginIcon from '@mui/icons-material/Login';

function LogIn() {
  const [value, setValue] = useState("")
  
  return (
    <Stack spacing={4}>
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
            <Button variant='contained' startIcon={<LoginIcon />}>Log In</Button>
        </Stack>
    </Stack>
  )
}

export default LogIn