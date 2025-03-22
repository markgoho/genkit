# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0

"""Utilities for working with messages."""

from genkit.core.typing import (
    Message,
    Metadata,
    Part,
    Role,
    TextPart,
)


def inject_instructions(
    messages: list[Message], instructions: str
) -> list[Message]:
    """
    Injects instructions into a list of messages.

    Args:
        messages: A list of MessageData objects.
        instructions: The instructions to inject, or False or None to skip injection.

    Returns:
        A new list of MessageData objects with the instructions injected,
        or the original list if injection was skipped.
    """
    if not instructions:
        return messages

    # bail out if a non-pending output part is already present
    if any(
        any(
            part.root.metadata
            and 'purpose' in part.root.metadata.root
            and part.root.metadata.root['purpose'] == 'output'
            and (
                'pending' not in part.root.metadata.root
                or not part.root.metadata.root['pending']
            )
            for part in message.content
        )
        for message in messages
    ):
        return messages

    new_part = Part(
        TextPart(text=instructions, metadata=Metadata({'purpose': 'output'}))
    )

    # find first message with purpose=output
    target_index = next(
        (
            i
            for i, message in enumerate(messages)
            if any(
                (
                    part.root.metadata
                    and 'purpose' in part.root.metadata.root
                    and part.root.metadata.root['purpose'] == 'output'
                    and 'pending' in part.root.metadata.root
                    and part.root.metadata.root['pending']
                )
                for part in message.content
            )
        ),
        -1,  # Default to -1 if not found
    )
    # find the system message or the last user message
    if target_index < 0:
        target_index = next(
            (
                i
                for i, message in enumerate(messages)
                if message.role == Role.SYSTEM
            ),
            -1,  # Default to -1 if not found
        )
    if target_index < 0:
        target_index = next(
            (
                i
                for i, message in reversed(list(enumerate(messages)))
                if message.role == 'user'
            ),
            -1,  # Default to -1 if not found
        )
    if target_index < 0:
        return messages

    m = Message(
        role=messages[target_index].role,
        # Create a copy of the content
        content=messages[target_index].content[:],
    )

    part_index = next(
        (
            i
            for i, part in enumerate(m.content)
            if part.root.metadata
            and 'purpose' in part.root.metadata.root
            and part.root.metadata.root['purpose'] == 'output'
            and 'pending' in part.root.metadata.root
            and part.root.metadata.root['pending']
        ),
        -1,  # Default to -1 if not found
    )
    if part_index >= 0:
        m.content[part_index] = new_part
    else:
        m.content.append(new_part)

    out_messages = messages[:]  # Create a copy of the messages list
    out_messages[target_index] = m

    return out_messages
